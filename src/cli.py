from src.chunkers.python_chunker import PythonChunker
from src.chunkers.markdown_chunker import MarkdownChunker
from src.models import MinimalSource
from typing import List
from src.indexer import Indexer
from src.ingestion import Ingestion
from src.retriever import Retriever


class RAGSystem:
    def __init__(
            self, index_path: str = "data/processed",
            raw_data_path: str = "data/raw/vllm-0.10.1") -> None:

        self.chunkers = {
            ".py": PythonChunker(),
            ".md": MarkdownChunker(),
            ".txt": MarkdownChunker()
        }
        self.ingestion: Ingestion = Ingestion(self.chunkers, raw_data_path)
        self.indexer: Indexer = Indexer(index_path)
        self.retriever: Retriever | None = None

    def index(self, max_chunk_size: int = 2000) -> None:
        self.indexer.build_index(self.ingestion.ingest(max_chunk_size))
        self.indexer.save()

    def search(self, question: str, k: int = 10) -> List[MinimalSource]:
        if self.retriever is None:
            self.indexer.load()
            self.retriever = Retriever(
                self.indexer.bm25_index, self.indexer.sources_metadata)
        return self.retriever.search(question, k)

    def search_dataset(self, dataset_path: str,
                       k: int = 10, save_directory: str = ...) -> None:
        pass

    def answer(self, question: str, k: int = 10) -> None:
        pass

    def answer_dataset(self, student_search_results_path: str,
                       save_directory: str = ...) -> None:
        pass

    def evaluate(self, student_answer_path: str,
                 dataset_path: str, k: int = 10) -> None:
        pass
