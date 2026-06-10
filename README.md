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