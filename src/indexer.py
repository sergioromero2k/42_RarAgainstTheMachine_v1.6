from src.models import MinimalSource
from typing import List, Tuple
import bm25s
import json


class Indexer:
    def __init__(self, index_path: str) -> None:
        self.index_path: str = index_path
        self.bm25_index: object = None
        self.sources_metadata: List[MinimalSource] = []

    def build_index(self, chunks: List[Tuple[MinimalSource, str]]) -> None:
        texts = []
        self.sources_metadata = []

        for src, text in chunks:
            texts.append(text)
            self.sources_metadata.append(src)

        tokens = bm25s.tokenize(texts)
        self.bm25_index = bm25s.BM25()
        self.bm25_index.index(tokens)

    def save(self) -> None:
        self.bm25_index.save(self.index_path)

        list_dict = []
        for src in self.sources_metadata:
            list_dict.append(src.model_dump())

        path_metadata = self.index_path + "/sources_metadata.json"
        with open(path_metadata, "w") as f:
            json.dump(list_dict, f)

    def load(self) -> None:
        self.bm25_index = bm25s.load(self.index_path)

        with open(path_metadata, "r")
