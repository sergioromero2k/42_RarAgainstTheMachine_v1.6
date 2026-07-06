* Chuking estrategico.
* BM25
* Recall@k.
* Integración de LLMs locales
* CLI profesional
* type safety.
* tqdm
* tranformers
* BM52/TF-IDF
* Qwen3-0.6B

### Sobre uv
uv esta escrito en Rust(no en python), y hace 2 cosas concretas que pip no hace bien:
* Genera un archivo `uv.lock` (nos piden pyproject.toml y uv.lock para dependecy management).
* Es muchisimo mas rapido resolviendo que versiones de cada paquete son compatibles entre sí.

#### uv.lock
El archivo uv.lock es como una foto exacta de qué versión de cada paquete (y de cada dependencia de cada paquete, hasta el último nivel) tenías instalada el día que lo generaste tú.
Es literalmente una lista gigante tipo:

```
transformers == 4.38.2
torch == 2.3.0
numpy == 1.26.4
tokenizers == 0.15.2
... (decenas más, incluso las que ni sabías que tenías)
```
Sin uv.lock, uv sync solo tiene el pyproject.toml para guiarse, que dice cosas flexibles tipo transformers>=4.30. Como no hay ninguna "foto exacta" que consultar, coge lo último disponible en ese momento — y ahí es donde puede romperse todo sin que tú hayas tocado una sola línea de código.


