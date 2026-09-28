.
├── docs/
├── src/
    |─── chunkers/
        |─── base_chunker.py
        |─── markdown_chunker.py
        |─── python_chunker.py

├── test/
├── level3.json
├── level4.json
├── level5.json
├── level6.json
├── level7.json
├── level8.json
├── level9.json
└── level10.json

## base_chunker
- Escogi base_chunker por que tenemos 2 formas de trocear codigo por encabezados y frases y por AST, funciones y clases, da igual devuelve siempre lo mismo List[MinimalSource].
- Tambien tener en cuenta que luego se usara en Ingestion, ya que este solo necesita saber si hay el metodo chunk().
- Uso ABC, @abstractmethod porque quiere que python te impida crear una instancia de BaseChunker a secas (no tiene sentido instanciarlo ya que es abstracto, mo un chunker real).
- Creo _save_fragment ya que tanto para python y markdown files el codigo es identico y devuelve lo mismo, no hay variacion ni forma distinta de hacerlo por ello.