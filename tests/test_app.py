import app


def test_make_pyqs_generates_search_links_and_files():
    papers = app.make_pyqs("JEE Main")

    assert [paper["year"] for paper in papers] == [2025, 2024]
    assert papers[0]["title"] == "JEE Main 2025"
    assert "JEE+Main+2025+previous+year+question+paper+pdf" in papers[0]["url"]
    assert papers[0]["file"] == "/papers/jee-main-2025.pdf"


def test_exam_record_adds_defaults_and_custom_fields():
    exam = app.exam_record(
        name="Sample Exam",
        category="Testing",
        description="A sample exam.",
        eligibility="Open eligibility.",
        syllabus=["Reasoning"],
        pattern="Objective test.",
        conducted_by="Sample Board",
        official_website="https://example.com",
        use_for="Demo admissions.",
        selection_process=["Apply", "Test"],
        notification="January",
        exam_date="March",
        duration="2 hours",
        exam_mode="Online",
        frequency="Annual",
    )

    assert exam["name"] == "Sample Exam"
    assert exam["dates"] == {"notification": "January", "examDate": "March"}
    assert exam["applicationMode"] == "Online"
    assert exam["fee"] == "Varies by category and notification"
    assert exam["books"]
    assert exam["preparationTips"]


def test_load_exams_assigns_ids_pyqs_and_application_steps():
    exams = app.load_exams()

    assert exams
    assert exams[0]["id"] == 1
    assert exams[0]["pyq"][0]["year"] == 2025
    assert exams[0]["applicationSteps"] == app.APPLICATION_STEPS
    assert len({exam["id"] for exam in exams}) == len(exams)


def test_matches_filters_by_query_and_category():
    exam = {
        "name": "Joint Entrance Examination",
        "description": "Engineering entrance exam",
        "category": "Engineering",
    }

    assert app.matches_filters(exam, "joint", "All categories")
    assert app.matches_filters(exam, "engineering", "Engineering")
    assert not app.matches_filters(exam, "medical", "Engineering")
    assert not app.matches_filters(exam, "joint", "Medical")
