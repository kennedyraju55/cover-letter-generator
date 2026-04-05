.PHONY: help install dev test lint run-cli run-web clean

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package
	pip install -e .

dev: ## Install with dev dependencies
	pip install -e ".[dev]"

test: ## Run tests
	python -m pytest tests/ -v --tb=short

lint: ## Run linting
	python -m py_compile src/cover_letter_gen/core.py
	python -m py_compile src/cover_letter_gen/cli.py

run-cli: ## Run CLI
	python -m cover_letter_gen.cli $(ARGS)

run-web: ## Launch Streamlit web UI
	streamlit run src/cover_letter_gen/web_ui.py

clean: ## Clean artifacts
	rm -rf build/ dist/ *.egg-info __pycache__ .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
