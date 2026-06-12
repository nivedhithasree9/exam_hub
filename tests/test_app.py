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


def test_matches_filters_supports_exam_acronyms_and_small_typos():
    exam = {
        "name": "National Eligibility cum Entrance Test (NEET UG)",
        "description": "Medical entrance exam",
        "category": "Medical",
        "conductedBy": "National Testing Agency",
        "logoText": "NEET",
    }

    assert app.matches_filters(exam, "neet", "All categories")
    assert app.matches_filters(exam, "neeet", "All categories")
    assert app.matches_filters(exam, "med", "Medical")


def test_build_ai_prompt_includes_exam_context_and_goal():
    exam = app.load_exams()[0]

    prompt = app.build_ai_prompt(exam, "Build a weekly revision plan.")

    assert "Indian competitive exams" in prompt
    assert "Joint Entrance Examination (JEE Main)" in prompt
    assert "Build a weekly revision plan." in prompt


def test_ask_ollama_uses_local_chat_payload(monkeypatch):
    captured = {}

    def fake_post_json(url, payload, headers=None, timeout=45):
        captured["url"] = url
        captured["payload"] = payload
        captured["headers"] = headers
        captured["timeout"] = timeout
        return {"message": {"content": "local answer"}}

    monkeypatch.setattr(app, "post_json", fake_post_json)

    answer = app.ask_ollama("http://localhost:11434/api/chat", "llama3.2", "hello")

    assert answer == "local answer"
    assert captured["url"] == "http://localhost:11434/api/chat"
    assert captured["payload"]["model"] == "llama3.2"
    assert captured["payload"]["stream"] is False
    assert captured["headers"] is None


def test_ask_openai_compatible_sends_bearer_token(monkeypatch):
    captured = {}

    def fake_post_json(url, payload, headers=None, timeout=45):
        captured["url"] = url
        captured["payload"] = payload
        captured["headers"] = headers
        captured["timeout"] = timeout
        return {"choices": [{"message": {"content": "byok answer"}}]}

    monkeypatch.setattr(app, "post_json", fake_post_json)

    answer = app.ask_openai_compatible("https://example.com/v1/chat/completions", "secret-token", "model-1", "hello")

    assert answer == "byok answer"
    assert captured["url"] == "https://example.com/v1/chat/completions"
    assert captured["payload"]["model"] == "model-1"
    assert captured["headers"] == {"Authorization": "Bearer secret-token"}


def test_format_ai_error_explains_ollama_connection_refused():
    message = app.format_ai_error(
        app.AI_PROVIDER_OLLAMA,
        "http://localhost:11434/api/chat",
        OSError("[WinError 10061] No connection could be made"),
    )

    assert "Start Ollama" in message
    assert "ollama run llama3.2" in message
    assert "host.docker.internal" in message
