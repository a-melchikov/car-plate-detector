run:
	uv run python app/main.py

download-model:
	python download_model.py

install:
	uv sync

setup:
	install download-model

lint:
	uv run ruff check app/

format:
	uv run ruff format app/
