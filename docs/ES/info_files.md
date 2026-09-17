BaseChunker (abstracta)
	- MarkdownChunker
	- PythonChunker

RAGSystem (orquestador central)
	- usa Ingestion -> usa BaseChunker (polimorfismo)
	- usa Indexer -> consume salida de Ingesion, guarda/carga índice
	- usa Retriever -> carga índice de Indexer, busca
	- usa Generator -> usa resultados de Retriever, genera texto.
	- usa Evaluator -> lee JSON con modelos Pydantic (independiente)

[Bonus] HybridRetriever compone Retriever -> SemanticRetriever

Ingestion -- usa (vía tipo BaseChunker) --> chunkers.
Indexer -- construye/guarda --> índice BM25 en disco.
Retriever -- carga/consulta --> índice BM25 en disco (el mismo que Indexer guardó).
RAGSystem crea y coordina -- Ingestion, Indexer, Retriever, Generator, Evaluator.

