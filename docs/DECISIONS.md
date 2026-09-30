# Decisiones de diseño

## Configuración de proyecto: `uv over pip/installs`
* `uv` está escrito en Rust, no en Python puro como `pip`. Usa caché global de paquetes y resolución de dependencias en paralelo, así que instalar o sincronizar dependencias es órdenes de magnitud más rápido.
* Con `pip` normalmente necesitas tres herramientas separadas — `venv` (crear el entorno), `pip` (instalar paquetes) y a veces `pip-tools` (generar lockfile). `uv` hace las tres cosas con un solo comando (`uv sync`), y genera automáticamente `uv.lock` — un `lockfile` que fija versiones exactas de todo el árbol de dependencias, para que el proyecto se reproduzca igual en cualquier máquina (la del evaluador, por ejemplo).

Esto se usa en 42 por que es mas fácil, si tu compañero clona el repo y hace `uv sync`, tiene que instalarse exactamente lo mismo que tú, sin sopresas de versiones.

## Pydantic models vs service class
* `BaseModel` sirve para validación automática al crear la instancia: si declaras `first_character_index: int` y alguien inerna crear el modelo con un string, Pydantic lanza un `ValidationError` automáticamente, sin que tú escribas ningún `if isinstance(...)`. Tambien permite la serialización/deserialización gratis `.model_dump_json()` convierte la instancia a JSON, `.model_validate_json()` hace el camino inverso. Esto es oro para tu proyecto, porque constantemente guardas/cargas cosas a disco (el dataset, los resultados de búsqueda, etc.) — sin Pydantic tendrías que escribir ese parseo a mano.
* `BaseModel` está pensado para **estructura de datos** cosas que principalmente se guardan, se cargan, se validan y se serializan a/desde  JSON. Su fortaleza es garantizar que los datos tienen la forma correcta.
* Los 8 modelos son todos estructuras de datos puras, se leen de JSON, se escriben en JSON, no tienen comportamiento propio. Por eso todos heredan de `BaseModel`, sin excepción.
