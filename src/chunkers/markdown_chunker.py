#!/usr/bin/env python3

from src.chunkers.base_chunker import BaseChunker
from src.models import MinimalSource


class MarkdownChunker(BaseChunker):

    def chunk(self, file_path, max_chunk_size=2000):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        paragraphs = content.split("\n\n")

        chunks = []
        current_position = 0

        for p in paragraphs:
            if not p:
                current_position += len("\n\n")
                continue

            init = current_position
            fin = init + len(p)

            if len(p) <= max_chunk_size:
                chunk = MinimalSource(
                    file_path=file_path,
                    first_character_index=init,
                    last_character_index=fin,
                )
                chunks.append(chunk)
            else:
                sub_init = 0
                while sub_init < len(p):
                    sub_fin = sub_init + max_chunk_size
                    chunk = MinimalSource(
                        file_path=file_path,
                        first_character_index=init + sub_init,
                        last_character_index=init + min(sub_fin, len(p)),
                    )
                    chunks.append(chunk)
                    sub_init = sub_fin
            current_position = fin + len("\n\n")
        return chunks
