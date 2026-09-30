# Decisiones de diseño

## Configuración de proyecto: `uv over pip/installs`
* `uv` está escrito en Rust, no en Python puro como `pip`. Usa caché global de paquetes y resolución de dependencias en paralelo, así que instalar o sincronizar dependencias es órdenes de magnitud más rápido.
* Con `pip` normalmente necesitas tres herramientas separadas — `venv` (crear el entorno), `pip` (instalar paquetes) y a veces `pip-tools` (generar lockfile). `uv` hace las tres cosas con un solo comando (`uv sync`), y genera automáticamente `uv.lock` — un `lockfile` que fija versiones exactas de todo el árbol de dependencias, para que el proyecto se reproduzca igual en cualquier máquina (la del evaluador, por ejemplo).

Esto se usa en 42 por que es mas fácil, si tu compañero clona el repo y hace `uv sync`, tiene que instalarse exactamente lo mismo que tú, sin sopresas de versiones.
