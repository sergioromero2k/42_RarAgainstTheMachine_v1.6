import bm25s

textos = [
    "def calcular_recall(resultados, ground_truth): return score",
    "How to configure the OpenAI compatible server in vLLM",
    "class LLMEngine: def __init__(self, model): pass",
]
corpus_tokens = bm25s.tokenize(textos)
print(corpus_tokens)

# Crear el índice y entrenarlo
retriever = bm25s.BM25()
retriever.index(corpus_tokens)

# Buscar algo
query = "how do I configure OpenAI server"
query_tokens = bm25s.tokenize(query)
resultados, scores = retriever.retrieve(query_tokens, k=2)

print(resultados)
print(scores)
