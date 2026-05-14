from src.models import AnsweredQuestion, MinimalSource

s = MinimalSource(
    file_path="fake/path.py", first_character_index=0, last_character_index=100
)
q = AnsweredQuestion(question="test", sources=[s], answer="respuesta")
print(q.question_id)
print(q.question)
print(q.model_dump_json())


MinimalSource(
    file_path="x.py", first_character_index="ESTO_ES_TEXTO", last_character_index=100
)
# ¿Lanza ValidationError?
