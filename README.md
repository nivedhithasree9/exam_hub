# Exam Hub

Exam Hub is a Streamlit app for browsing major Indian competitive exams. It brings
exam eligibility, syllabus, paper pattern, dates, books, preparation tips, official
links, and previous year question paper searches into one searchable interface.

The app is designed as a lightweight reference hub for students who want to compare
exam options quickly before visiting the official notification pages.

## Features

- Search exams by name or description
- Filter exams by category, including engineering, medical, law, management, defence,
  banking, civil services, and teaching
- Review exam facts such as conducting body, frequency, mode, duration, fees, and
  intended use
- Read eligibility, syllabus, selection process, preparation tips, application steps,
  recommended books, and official links
- Open previous year question paper searches from inside the app

## Requirements

- Python 3.12
- `pip`
- A modern browser

## Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Development Setup

Install runtime and development dependencies:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
pre-commit install
```

Run the main quality checks locally:

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

## Docker

Build and run the app in a container:

```bash
docker build -t exam-hub .
docker run --rm -p 8501:8501 exam-hub
```

Then open:

```text
http://localhost:8501
```

## Project Structure

- `app.py` - Streamlit app and exam data
- `requirements.txt` - Python dependencies
- `requirements-dev.txt` - Local quality, security, and test tools
- `pyproject.toml` - Shared Python tool configuration
- `.gitlab-ci.yml` - CI syntax check for the Streamlit app
- `.pre-commit-config.yaml` - Local hooks for formatting, linting, security, and audits
- `.specify/` - GitHub Spec Kit templates, scripts, workflows, and project memory
- `specs/` - Spec Kit feature specifications, plans, and task files

## Quality And Security

The repository includes automated checks for:

- Formatting and linting with Ruff
- Type checking with Mypy
- Additional quality checks with Flake8, Pylint, Vulture, and Pyupgrade
- Static security analysis with Bandit and Semgrep
- Secret scanning with Gitleaks or TruffleHog
- Dependency auditing with Pip Audit
- Test coverage enforcement with Pytest and Pytest Cov

## Configuration

The app does not require secrets for local development. Optional Streamlit server
settings are documented in `.env.example`.

## Spec Kit

This project includes GitHub Spec Kit for spec-driven development. Use these Codex skills when planning future changes:

```text
$speckit-constitution
$speckit-specify
$speckit-plan
$speckit-tasks
$speckit-implement
```

## License

Exam Hub is released under the AGPLv3 license. See `LICENSE` for details.
