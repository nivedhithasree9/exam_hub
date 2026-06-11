---
name: exam-hub-project
description: Use this skill when working on the Exam Hub Streamlit project, including exam data updates, UI changes, multilingual behavior, testing, compliance tooling, and documentation.
---

# Exam Hub Project Skill

## Project Context

Exam Hub is a Python Streamlit app for browsing competitive exams, filtering by category, viewing exam details, and opening official links, previous year paper searches, and recommended book shopping searches.

The main application lives in `app.py`. Tests live in `tests/test_app.py`.

## Common Tasks

- Add or update exam records in `BASE_EXAMS` or `ADDITIONAL_EXAMS`.
- Keep exam entries structured with eligibility, syllabus, pattern, dates, books, preparation tips, official website, and selection process.
- Preserve the sidebar search and category filtering behavior.
- Keep details inside the `st.dialog` popup opened by `View exam details`.
- Maintain multilingual support through `LANGUAGES`, `UI_TEXT`, `tr()`, and `translate_text()`.
- Use `make_book_links()` for recommended book shopping search links.

## UI Rules

- Keep the site clean, professional, and student-friendly.
- Do not show exam details automatically below result cards.
- Result cards should stay aligned across languages with fixed card heights and clamped text.
- The app should follow Streamlit Light/Dark theme variables instead of forcing one theme.
- Buttons must remain visible in both Light and Dark themes.

## Validation

Run these checks after changes:

```bash
ruff check app.py tests/test_app.py
pytest tests/test_app.py
```

If generated coverage files appear, remove `.coverage` before finishing.

## Safety Notes

- Do not remove existing compliance files or tooling unless explicitly requested.
- Do not hardcode product purchase pages; use search links so users can compare sellers and editions.
- Keep English as the default language and preserve English searchability for official exam names.
