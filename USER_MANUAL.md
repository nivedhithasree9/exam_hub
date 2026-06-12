Exam Hub User Manual
====================

Overview
--------

Exam Hub helps students browse and compare major Indian competitive exams from a
single Streamlit interface.

Using The App
-------------

1. Start the app with `streamlit run app.py`.
2. Open the local Streamlit URL shown in the terminal.
3. Use search to find exams by name or description.
4. Use category filters to narrow the list.
5. Open an exam detail view to review eligibility, syllabus, dates, selection
   process, books, application steps, preparation tips, official links, and
   previous year question paper searches.
6. Use the AI Assistant tab to generate study plans or preparation guidance.

AI Options
----------

The AI Assistant supports two modes:

- Local AI Inference: run Ollama locally and use the default Ollama chat
  endpoint, or enter another reachable Ollama endpoint.
- BYOK: select the OpenAI-compatible option and enter your own API token,
  endpoint, and model for that session. Use the built-in API key and chat API
  documentation links if you need to create a token.

API tokens are typed into the Streamlit session and are not saved in project
files. Always verify AI-generated advice against the latest official exam
notification.

Notes
-----

Exam details are reference material. Always verify deadlines, fees, eligibility,
and notification changes on the official exam website before applying.
