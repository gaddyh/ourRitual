# ourRitual

A Python application with a modular architecture.

## Project Structure

```
app/
  main.py              # Main entry point
  schemas.py           # Data schemas and models

  core/
    pipeline.py        # Main pipeline orchestration
    safety.py          # Safety checks and validation
    classifier.py      # Classification logic
    retriever.py       # Data retrieval
    planner.py         # Planning module
    responder.py       # Response generation
    evaluator.py       # Evaluation logic

  data/
    exercises.json     # Exercise data
    test_cases.json    # Test case data

  storage/
    memory_store.py    # Memory storage
    eval_store.py      # Evaluation storage
```

## Setup

1. Create and activate virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running

```bash
python app/main.py
```
