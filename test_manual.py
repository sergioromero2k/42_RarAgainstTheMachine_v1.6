from src.models import AnsweredQuestion, MinimalSource
from src.chunkers.markdown_chunker import MarkdownChunker

# s = MinimalSource(
#     file_path="fake/path.py", first_character_index=0, last_character_index=100
# )
# q = AnsweredQuestion(question="test", sources=[s], answer="respuesta")
# print(q.question_id)
# print(q.question)
# print(q.model_dump_json())


# MinimalSource(
#     file_path="x.py", first_character_index="ESTO_ES_TEXTO", last_character_index=100
# )
# # ¿Lanza ValidationError?

# chunker = MarkdownChunker()
# chunks = chunker.chunk("README.md", max_chunk_size=2000)

# for chunk in chunks:
#     print(chunk.first_character_index, "→", chunk.last_character_index)

# with open("README.md") as f:
#     content = f.read()

# for i, chunk in enumerate(chunks):
#     texto = content[chunk.first_character_index : chunk.last_character_index]
#     print(f"Chunk {i}: [{chunk.first_character_index} → {chunk.last_character_index}]")
#     print(texto[:80])  # solo los primeros 80 chars para no saturar
#     print("---")
