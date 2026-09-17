from pathlib import Path
from zipfile import ZipFile
from typing import List, Tuple, Dict
from src.models import MinimalSource
from src.chunkers.markdown_chunker import MarkdownChunker
from src.chunkers.python_chunker import PythonChunker
from src.chunkers.base_chunker import BaseChunker


class Ingestion:
    """"""
    def __init__(
            self, chunkers: dict[str, BaseChunker],
            raw_data_path: str = "data/raw/vllm-0.10.1") -> None:
        """"""
        self.chunkers: dict[str, BaseChunker] = chunkers
        self.raw_data_path: str = raw_data_path

    def ensure_repo_extracted(self) -> None:
        path = Path(self.raw_data_path)
        if not path.exists():
            zip_path = self.raw_data_path + ".zip"
            with ZipFile(zip_path, "r") as zip_file:
                zip_file.extractall("data/raw/")

    def ingest(self, max_chunk_size: int) -> List[Tuple[MinimalSource, str]]:
        self.ensure_repo_extracted()

        exten_valid = {".py", ".md", ".txt"}
        repo = Path(self.raw_data_path)

        for path in repo.rglob("*"):
            if path.is_file() and path.suffix.lower() in exten_valid:
                with open(path, "r") as f:
                    content = f.read()
                


