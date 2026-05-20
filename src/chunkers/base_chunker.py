#!/usr/bin/env python3

from abc import ABC, abstractmethod
from src.models import MinimalSource
from typing import List


class BaseChunker(ABC):

    @abstractmethod
    def chunk(
            self, file_path: str, max_chunk_size: int) -> List[MinimalSource]:
        pass
