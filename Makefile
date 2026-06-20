.PHONY: setup install playground test lint

setup:
	uvx google-agents-cli setup

install:
	uvx google-agents-cli install

playground:
	uv run adk web . --host 127.0.0.1 --port 8080

test:
	uv run pytest

lint:
	uvx google-agents-cli lint
