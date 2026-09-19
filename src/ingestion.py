from pathlib import Path
from zipfile import ZipFile
from typing import List, Tuple, Dict
from src.models import MinimalSource
from src.chunkers.markdown_chunker import MarkdownChunker
from src.chunkers.python_chunker import PythonChunker
from src.chunkers.base_chunker import BaseChunker


class Ingestion:
    """Loads repository files and splits them into chunks."""

    def __init__(
            self, chunkers: dict[str, BaseChunker],
            raw_data_path: str = "data/raw/vllm-0.10.1") -> None:
        """Initialize ingestion with chunkers and the repository path."""
        self.chunkers: dict[str, BaseChunker] = chunkers
        self.raw_data_path: str = raw_data_path

    def ensure_repo_extracted(self) -> None:
        """Extract the repository archive if it is not already available."""
        path = Path(self.raw_data_path)
        if not path.exists():
            zip_path = self.raw_data_path + ".zip"
            with ZipFile(zip_path, "r") as zip_file:
                zip_file.extractall("data/raw/")

    def ingest(self, max_chunk_size: int) -> List[Tuple[MinimalSource, str]]:
        """Read supported files and return
        their chunks with source metadata."""
        self.ensure_repo_extracted()
        repo = Path(self.raw_data_path)

        exten_valid = {".py", ".md", ".txt"}
        results = []

        for path in repo.rglob("*"):
            if path.is_file() and path.suffix.lower() in exten_valid:
                with open(path, "r") as f:
                    content = f.read()

                chunker = self.chunkers[path.suffix.lower()]
                sources = chunker.chunk(content, str(path), max_chunk_size)

                for src in sources:
                    text = content[
                        src.first_character_index:src.last_character_index]
                    results.append((src, text))
        return results
