from src.models import MinimalSource

s = MinimalSource(
    file_path="vllm/engine/llm.py",
    first_character_index=100,
    last_character_index=250
)
print("Objeto original: ", s)

s_json = s.model_dump_json()
print("JSON serializado: ", s_json)

s2 = MinimalSource.model_validate_json(s_json)
print("Objeto reconstruido: ", s2)
print("¿Son iguales?", s == s2)
