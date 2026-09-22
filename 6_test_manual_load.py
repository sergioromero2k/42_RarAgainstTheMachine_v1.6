from src.indexer import Indexer

idx = Indexer(index_path="data/processed")
idx.load()
print(f"Chunks cargados: {len(idx.sources_metadata)}")
print(idx.sources_metadata[0])
