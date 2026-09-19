from src.ingestion import Ingestion
from src.chunkers.markdown_chunker import MarkdownChunker
from src.chunkers.python_chunker import PythonChunker

chunkers = {
    ".py": PythonChunker(),
    ".md": MarkdownChunker(),
    ".txt": MarkdownChunker(),
}

ing = Ingestion(chunkers=chunkers)
ing.ensure_repo_extracted()
