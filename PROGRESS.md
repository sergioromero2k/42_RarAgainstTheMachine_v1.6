## 2026-10-14 — Día 10 (evaluador) — casi cerrado

-  `src/evaluator.py` con 5 funciones, todas probadas:
   - `iou`, `build_results_index`, `is_match` (mismo `file_path` + IoU >= 0.05)
   - `hit_at_k(retrieved, correct, k)`: ¿algún trozo de los k primeros acierta
     alguna fuente correcta? (dos `for` anidados sobre `retrieved[:k]` y `correct`)
   - `recall_at_k(results, dataset, k)`: fracción de preguntas con acierto
     (solo `AnsweredQuestion`, emparejando por `question_id`)
-  `RECALL_KS = (1, 3, 5, 10)` como constante (confirmar valores en el subject)
-  Primera medición real sobre docs (100 preguntas, k=10):
   recall@1 = 54%, @3 = 76%, @5 = 81%, @10 = 89%
   Crecen con k, como debe ser. Docs cumple el 80% en @5, con poco margen.

### Pendiente del Día 10
1. Separar `evaluate_files` (evaluator.py, sin `self`) del método `evaluate` (cli.py)
   y comprobar que el comando imprime 54.0, 76.0, 81.0 y 89.0
2. flake8 y mypy sobre evaluator.py y cli.py (import `UnansweredQuestion` sobrante,
   líneas largas, anotar el tipo de `index`)
3. Revisar la definición de recall en el subject: mi versión cuenta una pregunta
   como acierto si al menos una fuente coincide; el plan habla de "cuántas sources
   correctas se recuperaron" por pregunta. Comprobar el máximo de `sources` por
   pregunta y qué dice el subject.

### Próximo paso
Día 11 (CRÍTICO): `search_dataset` + `evaluate` sobre `dataset_code_public.json`
y anotar los números base de docs y code. Alerta del plan: recall@5 code < 40%
implica revisar el chunker Python (AST).