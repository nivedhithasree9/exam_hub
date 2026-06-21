# Exam Hub

Exam Hub is a Streamlit application for exploring major Indian competitive exams. It collects eligibility, syllabus, exam pattern, timelines, fees, books, preparation tips, official links, previous-year paper searches, and AI study guidance in one searchable interface.

The project is built for students who want to compare exam options quickly before reading the official notification in detail.

## Features

- Search exams by name, category, description, conducting body, or acronym.
- Filter exams across engineering, medical, law, management, defence, banking, civil services, teaching, and other categories.
- View structured exam details such as eligibility, pattern, mode, duration, fee, application mode, frequency, and use case.
- Read syllabus focus areas, selection process, preparation tips, recommended books, application steps, rules, and reservation guidance.
- Open official websites and previous-year question-paper searches.
- Switch UI labels and exam content into supported languages, including Telugu.
- Generate study guidance with Gemini, Google ADK, Groq BYOK, Free AI, or local Ollama.
- Use the Google ADK agent with exam tools and lightweight student memory.

## Tech Stack

- Python 3.12+
- Streamlit
- Google Agent Development Kit
- Pytest and pytest-cov
- Ruff, Flake8, Pylint, Mypy, Vulture, Pyupgrade
- Bandit, Semgrep, Gitleaks, pip-audit
- Pre-commit and pre-push hooks
- GitLab CI

## Project Structure

```text
.
|-- app.py                    # Streamlit app and exam data
|-- exam_hub_adk/             # Google ADK agent and tools
|-- tests/                    # Unit tests
|-- scripts/                  # Local compliance checks
|-- specs/                    # Spec-Kit feature specification
|-- .specify/                 # Spec-Kit configuration and templates
|-- .pre-commit-config.yaml   # Local quality hooks
|-- .gitlab-ci.yml            # CI pipeline
|-- .env.example              # Safe environment variable template
`-- requirements*.txt         # Runtime and development dependencies
```

## Requirements

- Python 3.12 or newer
- `pip`
- A modern browser
- Optional: Google AI Studio key for Gemini and ADK
- Optional: Ollama for local AI inference

## Quick Start

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install runtime dependencies:

```powershell
pip install -r requirements.txt
```

Create a private `.env` file from the example:

```powershell
copy .env.example .env
```

Edit `.env` and replace placeholder values as needed:

```text
GOOGLE_API_KEY=your_google_ai_studio_key
EXAM_HUB_ADK_MODEL=gemini-flash-latest
OLLAMA_CHAT_ENDPOINT=http://localhost:11434/api/chat
BYOK_CHAT_ENDPOINT=https://api.openai.com/v1/chat/completions
```

Run the app:

```powershell
streamlit run app.py
```

Open the URL shown by Streamlit, usually `http://localhost:8501`.

## Environment Variables

| Variable | Required | Purpose |
| --- | --- | --- |
| `GOOGLE_API_KEY` | Optional | Enables Gemini and Google ADK features. Keep this in `.env` or deployment secrets only. |
| `EXAM_HUB_ADK_MODEL` | Optional | Selects the ADK model. Defaults to `gemini-flash-latest`. |
| `OLLAMA_CHAT_ENDPOINT` | Optional | Ollama chat endpoint. Defaults to `http://localhost:11434/api/chat`. |
| `OLLAMA_ENDPOINT` | Optional | Alternate Ollama endpoint name also supported by the app. |
| `BYOK_CHAT_ENDPOINT` | Optional | OpenAI-compatible BYOK chat endpoint. |
| `BYOK_MODELS_ENDPOINT` | Optional | OpenAI-compatible model listing endpoint. |
| `BYOK_MODEL` | Optional | Default BYOK model. |
| `FREE_AI_ENDPOINT` | Optional | Free AI fallback endpoint. |

Do not commit `.env`. It is ignored by Git. Commit only `.env.example` with placeholders.

## AI Providers

Open any exam detail view and choose the **AI Assistant** tab.

- **Gemini AI**: Requires a Google AI Studio API key.
- **Google ADK Agent**: Uses `exam_hub_adk/agent.py` with tools for exam lookup, study planning, and student memory.
- **Free AI**: No API key required; falls back to built-in local guidance if the cloud endpoint is unavailable.
- **Ollama**: Requires Ollama running locally.
- **BYOK**: Uses your own API key with an OpenAI-compatible chat endpoint.

## Google ADK Agent

The ADK agent is defined in `exam_hub_adk/agent.py`. It can find exams, read exam details, build study plans, and save or recall lightweight student preparation memory.

For the Streamlit app, configure one Google key for the app or deployment:

```text
GOOGLE_API_KEY=your_google_ai_studio_key
```

Run the Streamlit app and choose **Google ADK Agent** in the AI Assistant tab.

You can also run the agent directly:

```powershell
adk run exam_hub_adk
```

For the ADK development web UI:

```powershell
adk web --port 8000
```

## Ollama Setup

Install and start Ollama, then pull a model:

```powershell
ollama pull llama3.2
ollama run llama3.2
```

Keep the endpoint as:

```text
OLLAMA_CHAT_ENDPOINT=http://localhost:11434/api/chat
```

If the app runs inside Docker, use:

```text
OLLAMA_CHAT_ENDPOINT=http://host.docker.internal:11434/api/chat
```

## Development Setup

Install development tools:

```powershell
pip install -r requirements-dev.txt
```

Install local Git hooks:

```powershell
pre-commit install --hook-type pre-commit --hook-type pre-push
```

Run all pre-commit checks manually:

```powershell
pre-commit run --hook-stage pre-commit --all-files
```

Run all pre-push checks manually:

```powershell
pre-commit run --hook-stage pre-push --all-files
```

## Testing

Run the test suite:

```powershell
python -m pytest
```

Run only app tests:

```powershell
python -m pytest tests\test_app.py
```

Coverage is enforced in `pyproject.toml`:

```text
--cov=. --cov-report=term --cov-fail-under=70
```

## Quality and Security Checks

The project uses:

- `ruff` and `ruff-format` for linting and formatting.
- `flake8` and `pylint` for additional lint checks.
- `mypy` for type checking.
- `vulture` for dead-code detection.
- `pyupgrade` for modern Python syntax.
- `bandit` and `semgrep` for static security checks.
- `gitleaks` for secret scanning.
- `pip-audit` for dependency vulnerability checks.
- `scripts/check_compliance.py` for required repository documentation and safe `.env.example` checks.

These checks run locally through pre-commit/pre-push hooks and in GitLab CI.

## GitLab CI

The GitLab pipeline includes:

- `lint`
- `format`
- `type_check`
- `security`
- `test`
- `coverage`

See `.gitlab-ci.yml` for exact commands.

## Docker

Build the image:

```powershell
docker build -t exam-hub .
```

Run the container:

```powershell
docker run --env-file .env -p 8501:8501 exam-hub
```

Open `http://localhost:8501`.

## Streamlit Cloud Deployment

1. Push the repository to GitLab/GitHub.
2. Create a Streamlit app from `app.py`.
3. Add secrets in the Streamlit app settings:

```toml
GOOGLE_API_KEY = "your_google_ai_studio_key"
EXAM_HUB_ADK_MODEL = "gemini-flash-latest"
```

4. Redeploy the app.

Never paste real API keys into `.env.example`, `README.md`, tests, or source code.

## Troubleshooting

### ADK uses fallback instead of Google

Check that `GOOGLE_API_KEY` is set in `.env` locally or Streamlit secrets in deployment. Restart the app after changing environment values.

### Ollama cannot connect

Start Ollama first:

```powershell
ollama run llama3.2
```

If using Docker, change the endpoint to `http://host.docker.internal:11434/api/chat`.

### Git blocks a push because of secrets

Remove the secret from the file and rotate the exposed key. Use `.env` or deployment secrets for real keys.

### Pre-commit says configuration is unstaged

Stage the hook config before committing:

```powershell
git add .pre-commit-config.yaml
```

## Contributing

Read `CONTRIBUTING.md` before opening changes. For local development, install the dev dependencies and hooks, run tests, and make sure no secrets are committed.

## Security

Read `SECURITY.md` for responsible disclosure. Do not open public issues containing secrets, private keys, tokens, exploit details, or private user data.

## License

This project is licensed under AGPLv3. See `LICENSE`.
