## 2026-10-01 — Día 7 (buffer semana 1, continuación)

-  flake8 limpio en src/
-  mypy: corregidos varios errores (self en cli.py, end_lineno en 
     python_chunker.py, bm25_index tipado como bm25s.BM25 | None)
-  mypy: quedan pendientes los errores de markdown_chunker.py 
     (TypedDict para fragments) y models.py:87 (List invariante en 
     StudentSearchResultsAndAnswer.search_results — usar Sequence)
-  Repasados y entendidos los 8 modelos Pydantic de models.py, con 
     sus relaciones de herencia:
     - AnsweredQuestion(UnansweredQuestion)
     - MinimalAnswer(MinimalSearchResults)
     - StudentSearchResultsAndAnswer(StudentSearchResults)
-  Creados docs/DECISIONS.md y PROGRESS.md en la raíz
-  Entradas en DECISIONS.md: "uv over pip/venv", "Pydantic models vs 
     service classes" (pendiente de pulir y añadir las de BaseChunker)

###  Próximo paso exacto
Resolver mypy models.py:87 usando `Sequence` en vez de `list` para el 
campo search_results (siguiendo la sugerencia del propio error de mypy). 
Después, introducir TypedDict en markdown_chunker.py para tipar 
fragments correctamente y cerrar el resto de errores mypy.

###  Backlog documental pendiente
- Terminar DECISIONS.md: BaseChunker (ya explicado, falta que tú lo 
  redactes), MarkdownChunker vs PythonChunker, Ingestion/Indexer sin 
  herencia, decisión de chunkers para .txt
- Seguir con Día 8 (Retriever) una vez cerrado el repaso completo