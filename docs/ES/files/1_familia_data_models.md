
## Familia 1 - Data Models (las 8 Pydantic)
No hacen nada por sí solos, no tienen lógica, son solo **contenedores de datos con firma fija**. Su única función es **"viajar"** entre las clases de servicio, llevando información de un lado a otro, y validarse a sí mismos.

## Familia 2 - Clases de servicio (todo lo demás)
`Ingestion`, `Indexer`, `Retriever`, `Generator`, `Evaluator`, `RAGSystem`, y tus chunkers. Estas sí tienen lógica, hacen cosas, y usan los `Data Models` como su "materia prima" de entrada y salida.

## MinimalSource
* Lo CREAN: `MarkdownChunker`, `PythonChunker` (dentro de chunk())
* Lo USAN: `Ingestion`, `Indexer`, `Retriever`, `Generator`, `Evaluator`
* vive DENTRO de: `AnsweredQuestion`, `MinimalSearchResults` (como listo)

`MinimalSource` es el formato de "dirección" que entiende el evaluador. Cuando al final de todo el pipeline tu sistema le diga a alguien **"la respuesta a tu pregunta está en este archivo, entre estos caracteres**, tiene que decírselo en exactamente esa forma (`file_path` + `first_character_index` + `last_character_index`), porque así es como el evaluador automatizado (moulinette) va a comparar tus resultados contra la solución correcta.

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
* lo CREA: `RAGSystem.search_dataaset()` (uno por cada pregunta con respuesta).
* contiene una lista de `MinimalSearchResults`

## MinimalAnswer
* lo CREA `RAGSystem.answer_dataset()` (uno por cada pregunta con respuesta).
* hereda de `MinimalSearchResults`.

## StudentSearchResults
* lo CREA/escribe: `RAGSystem.search_dataset()` (el JSON final de salida).
* contiene una lista de `MinimalSearchResults`.
* lo LEE: `Evaluator` (para comprar), `RAGSystem.answer_dataset()` (como entrada)

## StudentSearchResultsAndAnswer
* lo CREA/escribe: `RAGSystem.answer_dataset()` (el JSON final de salida)
* contiene una lista de `MinimalAnswer`.
