Contribution Guide
==================

Thank you for helping improve Exam Hub.

Development Workflow
--------------------

1. Create a branch for your change.
2. Install dependencies with `uv sync --group dev`.
3. Install hooks with `pre-commit install`.
4. Keep changes focused and update documentation when behavior changes.
5. Run the local quality checks before opening a merge request..

Local Checks
------------

Use these commands before submitting changes:

```bash
ruff check .
ruff format --check .
uv run ruff check .
uv run ruff format --check .
uv run mypy app.py exam_hub_adk tests scripts
uv run ty check
uv run bandit -c pyproject.toml -r app.py exam_hub_adk scripts
uv run pip-audit
pytest --cov=. --cov-report=term --cov-fail-under=70
```

Spec-Driven Changes
-------------------

For larger features, update the Spec Kit artifacts under `specs/` before
implementation. Keep the feature spec, plan, and task list aligned with the code.
