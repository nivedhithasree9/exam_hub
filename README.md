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
- Use a Google Agent Development Kit (ADK) agent with exam lookup, study-plan
  tools, and lightweight student memory
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

## Google ADK Agent

This project includes an ADK agent in `exam_hub_adk/agent.py`. It defines a
`root_agent` with Exam Hub tools for finding exams, reading exam details,
building study plans, and saving/recalling student preparation memory.

1. Create a Gemini key in Google AI Studio.
2. Set `GOOGLE_API_KEY` in your shell or `.env` file.
3. Install dependencies with `pip install -r requirements.txt`.
4. Run the Streamlit app and choose **Google ADK Agent** in the AI Assistant tab.

You can also run the agent directly with ADK:

```bash
adk run exam_hub_adk
```

For the ADK development web UI, run this from the repository root:

```bash
adk web --port 8000
```

## AI Options

Open any exam detail view and choose the **AI Assistant** tab.
Exam Hub supports Gemini, Google ADK, Groq BYOK, Free AI, and Ollama.

- Configure a default endpoint by setting the `GROQ_ENDPOINT` environment
  variable before launching the app, or enter an endpoint per-exam in the
  AI Assistant tab.
- If your GROQ endpoint requires authentication, provide a bearer token in the
  AI Assistant's "Bearer token" field. Tokens are entered into the Streamlit
  session and are not saved to the repository.

When running inside Docker, ensure the GROQ endpoint is reachable from the
container (for example, `http://host.docker.internal:<port>/...` on Docker
Desktop).
