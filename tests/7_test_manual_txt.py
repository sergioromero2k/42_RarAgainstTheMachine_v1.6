from src.chunkers.markdown_chunker import MarkdownChunker, MinimalSource


with open("my_test.txt", "r") as f:
    content = f.read()

m = MarkdownChunker()
v = m.chunk(content, "my_test.txt", 2000)
print(v)

