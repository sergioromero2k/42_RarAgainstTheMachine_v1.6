from src.indexer import Indexer
from src.retriever import Retriever

indexer = Indexer(index_path="data/processed")
indexer.load()

retriever = Retriever(indexer.bm25_index, indexer.sources_metadata)
results = retriever.search("tokenizer", k=3)

for source in results:
    with open(source.file_path, "r") as f:
        content = f.read()
    fragmento = content[source.first_character_index:source.last_character_index]
    print(f"--- {source.file_path} ---")
    print(fragmento)
    print()
