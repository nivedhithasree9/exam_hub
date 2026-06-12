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
- Generate AI-powered study guidance for a selected exam
- Use Local AI Inference through Ollama, or BYOK with your own token for an
  OpenAI-compatible chat completions endpoint

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

## AI Options

Open any exam detail view and choose the **AI Assistant** tab.

- Local AI: run Ollama on your machine, keep the provider set to `Local AI
  (Ollama)`, and use a model such as `llama3.2`.
- BYOK: choose `BYOK tokens (OpenAI-compatible)`, enter your own API token,
  endpoint, and model. Tokens are entered in the app session and are not stored
  in the repository. The app includes links to the OpenAI API keys page and chat
  completions API docs for users who need an API token.

When running inside Docker, use an Ollama endpoint reachable from the container,
for example `http://host.docker.internal:11434/api/chat` on Docker Desktop.
