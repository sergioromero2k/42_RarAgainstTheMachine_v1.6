## 2026-10-10 — Día 9 (search_dataset) — cerrado

-  `search_dataset(dataset_path, k, save_directory)` implementado en RAGSystem:
   lee RagDataset, itera las preguntas con tqdm, llama a `search()`, guarda
   StudentSearchResults con el mismo nombre del dataset dentro de `save_directory`
-  Datasets extraídos del zip a `data/datasets/{AnsweredQuestions,UnansweredQuestions}/`
-  Ejecutado sobre `UnansweredQuestions/dataset_docs_public.json` con k=10:
   100/100 preguntas procesadas, 10 MinimalSource por pregunta (~280 preguntas/s)
-  Rutas de mi salida (`data/raw/vllm-0.10.1/...`) coinciden con las del dataset de respuestas
-  `save_directory` por defecto: `data/output/search_results`; al medir paso
   la subcarpeta por tipo de dataset (si no, dos datasets con el mismo nombre
   se sobrescriben: limitación conocida, ver DECISIONS.md)
-  Teoría entendida: IoU (índice de Jaccard) = intersección / unión de rangos de
   caracteres; acierto si mismo `file_path` e IoU >= 0.05; recall@k = % de
   preguntas con algún acierto entre los k primeros resultados
-  Los 3 archivos: dataset sin respuestas (entrada), mis resultados, dataset con
   respuestas (solución). `evaluate` compara los dos últimos. Los datasets son
   públicos: no sobreajustar a esas preguntas
-  Problema resuelto: `uv` fallaba por `[tool.uv.workspace]` con `members = ["tests"]`
   en pyproject.toml; eliminada esa sección

### Observaciones para tuning (Días 11-13)
- Chunks casi duplicados (quark.py 3137-5110 y 3138-5111): revisar el cálculo del
  inicio tras el solape
- Chunks muy cortos (registration.md 0-310) en consultas sin relación (BM25 y documentos cortos)
- Stop words/stemming: siempre en Indexer y Retriever a la vez

## 2026-10-10 — Día 10 (evaluador) — en curso

-  Diseño claro: `evaluate` recibe mis resultados (StudentSearchResults) y el
   dataset con respuestas (RagDataset); solo las AnsweredQuestion tienen `sources`
-  Para cada pregunta: emparejar por `question_id`, mirar mis k primeros trozos,
   acierto si coincide la ruta y el IoU con alguna fuente correcta es >= 0.05

### Pendiente
1. Escribir `iou()` en `src/evaluator.py` y probarla (caso A ≈ 0,87; caso B = 0)
2. Diccionario `{question_id: retrieved_sources}` desde mis resultados
3. Acierto por pregunta con `isinstance` para las AnsweredQuestion
4. recall@1/3/5/10, comando `evaluate`, primera medición real