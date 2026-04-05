# Examples for Cover Letter Generator

This directory contains example scripts demonstrating how to use this project.

## Quick Demo

```bash
python examples/demo.py
```

## What the Demo Shows

- **`load_config()`** — Call load_config
- **`get_tones()`** — Call get_tones
- **`read_file()`** — Read content from a text file.
- **`extract_skills()`** — Extract skills from text and categorize them.
- **`match_skills()`** — Create a skill matching matrix between resume and job description.

## Prerequisites

- Python 3.10+
- Ollama running with Gemma 4 model
- Project dependencies installed (`pip install -e .`)

## Running

From the project root directory:

```bash
# Install the project in development mode
pip install -e .

# Run the demo
python examples/demo.py
```
