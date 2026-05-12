install:
	uv sync

run:
	uv run src

debug:
	DEBUG=1 uv run src
	
lint:
    uv run flake8 .
    uv run mypy . --warn-return-any --warn-unused-ignores \
        --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs


clean:
	rm -rf __pycache__ 
