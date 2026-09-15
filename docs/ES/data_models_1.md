## MinimalSource
* Lo CREAN: `MarkdownChunker`, `PythonChunker` (dentro de chunk())
* Lo USAN: `Ingestion`, `Indexer`, `Retriever`, `Generator`, `Evaluator`
* vive DENTRO de: `AnsweredQuestion`, `MinimalSearchResults` (como listo)

## UnansweredQuestion
* se LEE desde JSON (por `RAGSystem.search_dataset`, usando `RagDataset`)

## AnsweredQuestion
* Se LEE desde JSON (por Evaluator, como "ground truth")
* hereda de `UnansweredQuestion`

## RagDataset
* lo USA: `RAGSystem.search_dataset()` (para leer el archivo de preguntas)
* lo USA: `Evaluator` (para leer el archivo de "solución correcta")
* contiene una lista de `AnsweredQuestion` | `UnansweredQuestion`

## MinimalSearchResults