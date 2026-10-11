## 2026-10-11 — Día 10 (evaluador) — en curso

-  `src/evaluator.py` creado con 3 piezas, todas probadas a mano:
   - `iou(a_start, a_end, b_start, b_end)`: intersección / unión de rangos de
     caracteres; devuelve 0.0 si no se solapan o si la unión es 0.
     Pruebas: (100,200,150,250) = 0.333; (4695,6098,4495,6100) = 0.874; sin solape = 0.0
   - `build_results_index(results)`: `{question_id: retrieved_sources}` para buscar
     en O(1) por pregunta en vez de recorrer la lista. Prueba: 100 preguntas, 10 trozos cada una
   - `is_match(retrieved, correct)`: acierto si mismo `file_path` (se comprueba
     primero) e IoU >= `IOU_THRESHOLD` (0.05, fijado por el subject)
-  Teoría entendida: el IoU (índice de Jaccard) divide entre la unión para que un
   chunk gigante no puntúe alto solo por contener la respuesta

### Pendiente del Día 10
1. `hit_at_k(retrieved, correct, k)`: ¿algún trozo de los k primeros acierta alguna
   fuente correcta? (dos `for` anidados sobre `retrieved[:k]` y `correct`, con `is_match`)
2. Recall@k: por cada pregunta del dataset con respuestas (`isinstance` a
   `AnsweredQuestion`), emparejar por `question_id` con el índice y contar aciertos
   para k = 1, 3, 5, 10
3. Comando `evaluate(student_answer_path, dataset_path, k)` en RAGSystem
4. Primera medición real sobre docs (100 preguntas) y apuntarla aquí

### Próximo paso
Escribir `hit_at_k` y probarla con el test de los 3 trozos (esperado: False con k=1, True con k=2).