import app


def test_make_pyqs_generates_search_links_and_files():
    papers = app.make_pyqs("JEE Main")

    assert [paper["year"] for paper in papers] == [2025, 2024]
    assert papers[0]["title"] == "JEE Main 2025"
    assert "JEE+Main+2025+previous+year+question+paper+pdf" in papers[0]["url"]
    assert papers[0]["file"] == "/papers/jee-main-2025.pdf"


def test_make_book_links_generates_shopping_searches():
    links = app.make_book_links("GMAT Official Guide")

    assert links["Amazon"] == "https://www.amazon.in/s?k=GMAT+Official+Guide"
    assert links["Flipkart"] == "https://www.flipkart.com/search?q=GMAT+Official+Guide"


def test_tr_uses_language_value_and_english_fallback():
    assert app.tr("search_exams", "hi") == "परीक्षा खोजें"
    assert app.tr("curated_exams", "hi") == "Curated exams"


def test_translate_text_returns_english_without_translation():
    assert app.translate_text("Exam Hub", "en") == "Exam Hub"


def test_translate_text_falls_back_when_translation_request_fails(monkeypatch):
    def fail_request(*_args, **_kwargs):
        raise TimeoutError

    monkeypatch.setattr(app, "urlopen", fail_request)
    app.translate_text.clear()

    assert app.translate_text("Exam Hub", "hi") == "Exam Hub"


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


def test_make_exam_logo_text_uses_aliases_and_fallbacks():
    assert app.make_exam_logo_text({"name": "Joint Entrance Examination (JEE Main)"}) == "JEE"
    assert app.make_exam_logo_text({"name": "Sample Professional Aptitude Test"}) == "SPAT"


def test_load_exams_assigns_ids_pyqs_and_application_steps():
    exams = app.load_exams()

    assert exams
    assert exams[0]["id"] == 1
    assert exams[0]["logoText"] == "JEE"
    assert all(exam["logoText"] for exam in exams)
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
