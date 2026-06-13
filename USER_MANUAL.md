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

The AI Assistant runs GROQ queries against a configured endpoint.

- Set a default endpoint using the `GROQ_ENDPOINT` environment variable before
  launching the app, or paste an endpoint into the "GROQ endpoint" field in
  the AI Assistant tab for a specific exam.
- If required, provide a bearer token in the "Bearer token" field; the token
  is used only for the current session and is not persisted in the repository.
- Enter a GROQ query in the query box and click "Run GROQ query" to execute it
  and view JSON results in the UI. Example query:

```
*[_type == "exam" && name == "Joint Entrance Examination (JEE Main)"]
```

Always verify any data or advice returned by a remote endpoint against the
official exam notification before acting on it.

Notes
-----

Exam details are reference material. Always verify deadlines, fees, eligibility,
and notification changes on the official exam website before applying.
