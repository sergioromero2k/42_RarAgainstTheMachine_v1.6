# Ingestion
---
### Por qué devolver la tupla (`MinimalSource`, texto)
---
Piensa en quién va a usar este resultado: `Indexer`, en el siguiente paso del pipeline. 
Indexer necesita dos cosas distintas para cada chunk:
* **El texto real** — porque BM25 necesita palabras para poder compararlas contra las preguntas de los usuarios
* **El MinimalSource** — porque, cuando BM25 encuentre que ese chunk es relevante para una pregunta, necesita poder decirle al usuario dónde está esa información (qué archivo, qué posición), no solo devolverle el texto suelto.
