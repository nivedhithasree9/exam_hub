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

The AI Assistant can generate study plans and preparation guidance with the
supported providers shown in the app.

- Use Gemini AI with a Google AI Studio API key.
- Use the Google ADK Agent with the app's configured Google API key.
- Use Free AI without an API key; the app falls back to built-in guidance if
  the cloud endpoint is unavailable.
- Use Ollama when a local Ollama server is running.

Always verify any data or advice returned by a remote endpoint against the
official exam notification before acting on it.

Notes
-----

Exam details are reference material. Always verify deadlines, fees, eligibility,
and notification changes on the official exam website before applying.
