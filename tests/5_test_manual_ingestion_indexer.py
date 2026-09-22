from src.ingestion import Ingestion
from src.indexer import Indexer
from src.chunkers.markdown_chunker import MarkdownChunker
from src.chunkers.python_chunker import PythonChunker
import time

chunkers = {
    ".py": PythonChunker(),
    ".md": MarkdownChunker(),
    ".txt": MarkdownChunker()
}

start = time.time()
ingestion = Ingestion(chunkers=chunkers)
resultado = ingestion.ingest(max_chunk_size=2000)

print(f"Total de chunks generados: {len(resultado)}")

indexer = Indexer(index_path="data/processed")
indexer.build_index(resultado)
indexer.save()

print("Indice guardado correctamente.")
print(f"Tiempo: {time.time() - start:.2f}s")
