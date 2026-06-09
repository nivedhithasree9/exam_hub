Contribution Guide
==================

Thank you for helping improve Exam Hub.

Development Workflow
--------------------

1. Create a branch for your change.
2. Install dependencies with `pip install -r requirements.txt` and
   `pip install -r requirements-dev.txt`.
3. Install hooks with `pre-commit install`.
4. Keep changes focused and update documentation when behavior changes.
5. Run the local quality checks before opening a merge request.

Local Checks
------------

Use these commands before submitting changes:

```bash
ruff check .
ruff format --check .
mypy .
bandit -c pyproject.toml -r .
flake8 .
pylint app.py
vulture --min-confidence 100 .
pip-audit -r requirements.txt
pytest --cov=. --cov-report=term --cov-fail-under=70
```

Spec-Driven Changes
-------------------

For larger features, update the Spec Kit artifacts under `specs/` before
implementation. Keep the feature spec, plan, and task list aligned with the code.
