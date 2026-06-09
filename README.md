# Exam Hub

Exam Hub is a Streamlit app for browsing major Indian competitive exams, including eligibility, syllabus, pattern, dates, books, preparation tips, official links, and previous year question paper searches.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Project Structure

- `app.py` - Streamlit app and exam data
- `requirements.txt` - Python dependencies
- `.gitlab-ci.yml` - CI syntax check for the Streamlit app
- `.specify/` - GitHub Spec Kit templates, scripts, workflows, and project memory
- `specs/` - Spec Kit feature specifications, plans, and task files

## Features

- Search exams by name or description
- Filter by category
- View exam facts, eligibility, syllabus, selection process, books, preparation tips, application steps, and official links
- Open previous year question paper searches from inside the app

## Spec Kit

This project includes GitHub Spec Kit for spec-driven development. Use these Codex skills when planning future changes:

```text
$speckit-constitution
$speckit-specify
$speckit-plan
$speckit-tasks
$speckit-implement
```
