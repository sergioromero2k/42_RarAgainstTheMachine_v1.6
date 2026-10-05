## 2026-10-03 — Día 8 (Retriever) — cerrado

-  Retriever construido, probado y conectado a RAGSystem (lazy loading)
-  Teoría repasada: BM25 en tiempo de query, stop words, stemming, 
     y por qué la tokenización debe ser idéntica entre index-time y 
     query-time (mismo bm25s.tokenize() en ambos lados)
-  Nota para tuning futuro (Días 12-13): si el recall es bajo, 
     considerar añadir stop words/stemming — pero aplicarlo siempre 
     en Indexer y Retriever a la vez, nunca en uno solo

###  Próximo paso
Día 9: implementar search_dataset(dataset_path, k, save_directory) 
en RAGSystem — leer RagDataset desde JSON, iterar preguntas, llamar 
a search() por cada una, guardar StudentSearchResults.