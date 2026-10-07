# Decisiones de diseño

## Configuración de proyecto: `uv over pip/installs`
* `uv` está escrito en Rust, no en Python puro como `pip`. Usa caché global de paquetes y resolución de dependencias en paralelo, así que instalar o sincronizar dependencias es órdenes de magnitud más rápido.
* Con `pip` normalmente necesitas tres herramientas separadas — `venv` (crear el entorno), `pip` (instalar paquetes) y a veces `pip-tools` (generar lockfile). `uv` hace las tres cosas con un solo comando (`uv sync`), y genera automáticamente `uv.lock` — un `lockfile` que fija versiones exactas de todo el árbol de dependencias, para que el proyecto se reproduzca igual en cualquier máquina (la del evaluador, por ejemplo).

Esto se usa en 42 por que es mas fácil, si tu compañero clona el repo y hace `uv sync`, tiene que instalarse exactamente lo mismo que tú, sin sopresas de versiones.

## Pydantic models vs service class
* `BaseModel` sirve para validación automática al crear la instancia: si declaras `first_character_index: int` y alguien inerna crear el modelo con un string, Pydantic lanza un `ValidationError` automáticamente, sin que tú escribas ningún `if isinstance(...)`. Tambien permite la serialización/deserialización gratis `.model_dump_json()` convierte la instancia a JSON, `.model_validate_json()` hace el camino inverso. Esto es oro para tu proyecto, porque constantemente guardas/cargas cosas a disco (el dataset, los resultados de búsqueda, etc.) — sin Pydantic tendrías que escribir ese parseo a mano.
* `BaseModel` está pensado para **estructura de datos** cosas que principalmente se guardan, se cargan, se validan y se serializan a/desde  JSON. Su fortaleza es garantizar que los datos tienen la forma correcta.
* Los 8 modelos son todos estructuras de datos puras, se leen de JSON, se escriben en JSON, no tienen comportamiento propio. Por eso todos heredan de `BaseModel`, sin excepción.

### Models
* `MinimalSource` un fragmento de archivo: `ruta` + `índice de carácter`. Es el bloque atómica que usan casi todos los demás modelos para citar de dónde sale la información.
* `UnansweredQuestion` — una pregunta sin responder: question_id (autogenerado con default_factory, como ya vimos) + el texto. Es la entrada "cruda" del dataset.
* `AnsweredQuestion(UnansweredQuestion)` — hereda de la anterior porque es una pregunta, pero con extras: `sources` (dónde está la respuesta real) y `answer`.
* `RagDataset` el contenedor del `dataset` completo: una lista de preguntas que pueden ser `AnsweredQuestion` o `UnansweredQuestion` (con el |, un `Union`). 
* `MinimalSearchResults` — el resultado de buscar **(no responder)** una pregunta: su `question_id`, el texto, y los `retrieved_sources` que encontró tu `Retriever`.
* `MinimalAnswer(MinimalSearchResults)` hereda porque además de los resultados de búsqueda, añade el campo `answer` generado por el **LLM**. Mismo patrón que `AnsweredQuestion`/`UnansweredQuestion`: "es un resultado de búsqueda + la respuesta generada".
* `StudentSearchResults` el resultado de correr `search_dataset` sobre todo el dataset: una lista de `MinimalSearchResults` + el `k` usado. Es el contenedor de nivel superior, no una pregunta individual.
* `StudentSearchResultsAndAnswer(StudentSearchResults)` — hereda de `StudentSearchResults`, pero sobrescribe search_results para que ahora sea una lista de `MinimalAnswer` (con respuesta) en vez de `MinimalSearchResults` (sin respuesta).

## Ingestion & Indexer
`Ingestion` se encarga de **leer el repositorio de vLLM y trocearlo.**
Concretamente:
* Si el repo no está descomprimido en disco, lo descomprime automáticamente (`ensure_repo_extracted()`).
* Recorre todos los archivos del repo(`rglob`), filtrando solo `.py`, `.md`, `.txt`.
* Para cada archivo, elige el chunker correcto según su extensión, y lo trocea en fragmentos (`MinimalSource` + el texto real de ese fragmento).
* Devuelve la lista completa de (`MinimalSource`, texto) de todo el repo.

`Indexer` se encarga de **construir**, **guardar** y **cargar** el índice de búsqueda `BM25` a partir de esos chunks. 
Concretamente:
* `build_index()` coge la lista de `(MinimalSource, texto)` que le da `Ingestion`, separa los textos de los metadatos en 2 listas, paralelas, tokeniza los textos, y construye el índice BM25 con `bm25s`.
* `save()`: guarda ese índice y la lista de metadatos a disco (**data/processed/**).
* `load()`: recupera ambas cosas desde disco para usarlas de nuevo sin tener que reconstruir todo.

## Indexer & Retriever
* `Indexer` responsable de **construir y persistir** el índice de búsqueda: toma los chunks ya troceados, los tokeniza, construye el índice **BM25** en memoria, y lo guarda/carga de disco (`build_index()`, `save()`, `load()`). Es la parte **"offline"** del sistema - se ejecuta una vez (en el comando `index`), no en cada búsqueda.

* `Retriever` responsable de **buscar en tiempo real** sobre un índice ya construido: recibe el `bm25_index` y `sources_metadata` ya cargados, tokeniza la `query` del usuario de la misma forma que se tokenizó al `indexar`, y devuelve los top-k `MinimalSource` más relevantes. Es la parte **"online"** — se ejecuta en cada llamada a `search()`, `Retriever` no responde, solo recupera — te da una lista ordenada de los chunks más relevantes (como fragmentos de evidencia), y nada más. Esa lista luego la usan otras piezas: tú mismo la usas directamente en el comando **search()** (para enseñarle al evaluador qué encontró), y más adelante `Generator` la usa como contexto para redactar la respuesta en lenguaje natural con **Qwen3**.

### Ejemplo
* `Ingestion` es la que va primero: abre el repo de vLLM (lo descomprime si hace falta), recorre todos los archivos `.py`, `.md` y `.txt`, y a cada uno lo trocea con su chunker. Devuelve una lista de pares: el `MinimalSource` (archivo + dónde empieza y acaba el trozo) y el texto de ese trozo. No busca nada ni construye ningún índice, solo prepara los trozos.
* `Indexer` coge esos trozos, tokeniza los textos y hace algo como un diccionario: palabra -> en qué chunks sale y cuántas veces. Eso se guarda tal cual en el índice.
* `Retriever` coge la pregunta, la tokeniza igual, mira ese diccionario a ver qué chunks tienen más coincidencia con las palabras de la pregunta, y devuelve los **top-k**. No da respuesta, solo busca y trae lo más parecido.

Orden: `Ingestion` (trocea) -> `Indexer` (indexa) -> `Retriever` (busca).

## search_dataset
`search()` responde a una pregunta suelta, pensada para probar a mano desde la terminal. Pero con una sola pregunta no puedes saber si tu sistema es bueno. Para eso necesitas medirlo con muchas preguntas, y `search_dataset` es lo que permite medirlo.

* El dataset (`dataset_docs_public.json`) es una lista de preguntas, por ejemplo 100.
* `search_dataset` le hace todas esas preguntas a tu `Retriever` y apunta, para cada una, qué chunks ha recuperado.
* Guarda todo en un archivo JSON(`StudentSearchResults`). Ese archivo es tu **tu hoja de respuestas del examen.**
* Luego alguien corrige esa hoja comparándola con las respuestas correctas (el dataset `AnsweredQuestions`): la `moulinette` en la defensa, y tu propio evaluate (el Día 10) mientras desarrollas. De ahí sale el **recall@k**.

**Tunnig(ajuste, o afinado)** es cambiar los parámetros o decisiones de tu sistema para que acierte más, midiendo el efecto de cada cambio. Un ejemplo con tu proyecto: pruebas `max_chunk_size=2000`, mides el recall, lo bajas a 1000, vuelves a medir y te quedas con el que dé mejor resultado.

## IoU (Intersection over Union)
* El **IoU** **no** compara respuestas escritas, compara sitios del archivo.
* **IoU** no es un algoritmo complejo, es una métrica: una fórmula que da un número entre 0 y 1 para decir cuánto se parecen dos cosas. Se calcula en tres operaciones (mínimo, máximo, una división). También se llama índice de Jaccard (lo propuso Paul Jaccard a principios del siglo XX para comparar conjuntos). Tu caso es la versión más simple: en vez de cuadros en 2D, son rangos en una línea (casillas de un archivo, 1D).


Es la medida de cuánto se solapan dos rangos de caracteres: la parte común dividida por la parte total que cubren entre los dos. Vale 1 si coinciden del todo y 0 si no se tocan. En este proyecto se usa para decidir si un `chunk` tuyo "acierta" respecto al fragmento correcto del dataset.

* **Lo que ellos te dan:** para cada pregunta, el lugar exacto donde está la información. Por ejemplo, "en lora.md, casillas 4695 a 6098".
* **Lo que genera tu sistema:** para cada pregunta, 10 trozos que cree que contienen la información. Cada uno con su archivo y sus casillas.
* **Lo que mide el IoU:** si alguno de tus 10 trozos cae en el mismo sitio que el de ellos.
