## 2026-10-05 / 2026-10-07 — Día 9 (search_dataset) — funcional, con cabos sueltos

-  `search_dataset` implementado y ejecutado sobre
   `UnansweredQuestions/dataset_docs_public.json` con k=10 (10 fuentes por pregunta)
-  Datasets extraídos del zip a `data/datasets/{AnsweredQuestions,UnansweredQuestions}/`
-  Rutas de mi salida (`data/raw/vllm-0.10.1/...`) coinciden con las del dataset de respuestas
-  Teoría entendida: IoU (índice de Jaccard) = intersección / unión de rangos
   de caracteres; acierto si mismo `file_path` e IoU >= 0.05; recall@k = % de
   preguntas con algún acierto en los k primeros resultados
-  Los 3 archivos: dataset sin respuestas (entrada), mis resultados, dataset con
   respuestas (solución). `evaluate` compara los dos últimos. Los datasets son
   públicos: no sobreajustar a esas preguntas.

### Pendiente del Día 9
- Imports que faltan en cli.py, `tqdm` en el bucle
- Decidir `save_directory` (por defecto u obligatorio) y apuntar el porqué en DECISIONS
- Comprobar nº de preguntas del resultado = nº del dataset

### Observaciones para tuning (Días 11-13)
- Chunks casi duplicados (quark.py 3137-5110 y 3138-5111): revisar cálculo
  del inicio tras el solape
- Chunks muy cortos (registration.md 0-310) en consultas sin relación
- Stop words/stemming: siempre en Indexer y Retriever a la vez

## 2026-10-07 — Día 10 (evaluador) — en curso

-  Paso 1 de 6: escribir `iou()` en `src/evaluator.py` (pendiente de escribir)

### Próximo paso
Escribir `iou()` yo, probarla (caso A ≈ 0,87; caso B = 0). Luego: leer los dos
archivos con los modelos Pydantic, acierto por pregunta, recall@1/3/5/10,
comando `evaluate`, primera medición real.