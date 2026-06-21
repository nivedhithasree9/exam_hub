from io import BytesIO
from urllib.error import HTTPError

import app
from exam_hub_adk import tools as adk_tools


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


def test_telugu_ui_overrides_cover_visible_home_labels():
    visible_keys = [
        "app_name",
        "hero_copy",
        "curated_exams",
        "current_matches",
        "all_categories",
        "exam_details",
        "ai_assistant",
        "eligibility",
        "exam_pattern",
        "conducted_by",
        "frequency",
        "before_you_apply",
        "question_paper",
    ]

    for key in visible_keys:
        assert app.tr(key, "te") != app.tr(key, "en")


def test_category_display_name_translates_all_categories_without_changing_filter_value():
    assert app.category_display_name("All categories", "te") == app.tr("all_categories", "te")
    assert app.matches_filters(
        {"name": "Sample", "description": "Engineering exam", "category": "Engineering"},
        "",
        "All categories",
    )


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
    assert "Build a weekly revision plan." in prompt


def test_query_groq_requires_endpoint():
    try:
        app.query_groq("", "", '*[_type == "exam"]')
    except ValueError as exc:
        assert "GROQ endpoint is required" in str(exc)
    else:
        raise AssertionError("Expected ValueError when endpoint is empty")


def test_gemini_ai_is_default_provider():
    assert app.AI_PROVIDER_OPTIONS[0] == app.AI_PROVIDER_GEMINI


def test_adk_agent_is_available_as_ai_provider():
    assert app.AI_PROVIDER_ADK in app.AI_PROVIDER_OPTIONS
    assert app.DEFAULT_ADK_MODEL == "gemini-flash-latest"


def test_ollama_default_endpoint_matches_env_example():
    assert app.DEFAULT_OLLAMA_URL == "http://localhost:11434/api/chat"


def test_load_local_env_sets_missing_values_only(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("EXAM_HUB_TEST_KEY=from-file\nEXAM_HUB_EXISTING=from-file\n", encoding="utf-8")
    monkeypatch.delenv("EXAM_HUB_TEST_KEY", raising=False)
    monkeypatch.setenv("EXAM_HUB_EXISTING", "from-env")

    app.load_local_env(env_file)

    assert app.getenv("EXAM_HUB_TEST_KEY") == "from-file"
    assert app.getenv("EXAM_HUB_EXISTING") == "from-env"


def test_ensure_adk_google_api_key_uses_packaged_key(monkeypatch):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_GENAI_USE_VERTEXAI", raising=False)
    monkeypatch.setenv("EXAM_HUB_GOOGLE_API_KEY", " packaged-key ")

    assert app.ensure_adk_google_api_key() is True
    assert app.getenv("GOOGLE_API_KEY") == "packaged-key"


def test_ensure_adk_google_api_key_reports_missing_configuration(monkeypatch):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("EXAM_HUB_GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_GENAI_USE_VERTEXAI", raising=False)
    monkeypatch.setattr(app, "get_streamlit_secret", lambda _name: "")

    assert app.ensure_adk_google_api_key() is False


def test_ask_gemini_sends_generate_content_payload(monkeypatch):
    captured = {}

    def fake_post_json(url, payload, headers=None, timeout=45):
        captured["url"] = url
        captured["payload"] = payload
        captured["headers"] = headers
        captured["timeout"] = timeout
        return {"candidates": [{"content": {"parts": [{"text": "Gemini answer"}]}}]}

    monkeypatch.setattr(app, "post_json", fake_post_json)

    answer = app.ask_gemini("  gemini-key\n", "gemini-3.5-flash", "hello exam")

    assert answer == "Gemini answer"
    assert captured["url"].endswith("/gemini-3.5-flash:generateContent")
    assert captured["payload"]["contents"][0]["parts"][0]["text"] == "hello exam"
    assert captured["payload"]["generationConfig"]["maxOutputTokens"] == 700
    assert captured["headers"] == {"x-goog-api-key": "gemini-key"}
    assert captured["timeout"] == 60


def test_ask_free_ai_uses_no_key_endpoint(monkeypatch):
    captured = {}

    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def read(self):
            return b"Free AI answer"

    def fake_urlopen(request, timeout=60):
        captured["url"] = request.full_url
        captured["headers"] = dict(request.header_items())
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr(app, "urlopen", fake_urlopen)

    answer = app.ask_free_ai("hello exam")

    assert answer == "Free AI answer"
    assert captured["url"].startswith(app.DEFAULT_FREE_AI_URL)
    assert "Authorization" not in captured["headers"]
    assert captured["timeout"] == 60


def test_free_ai_rate_limit_can_use_builtin_backup():
    exam = app.load_exams()[0]
    backup = app.build_local_study_response(exam, "what is the syllabus")

    assert "Main syllabus areas" in backup
    assert "30-day structure" not in backup


def test_no_key_assistant_falls_back_to_builtin_response(monkeypatch):
    exam = app.load_exams()[0]

    def fail_free_ai(_prompt):
        raise TimeoutError

    monkeypatch.setattr(app, "ask_free_ai", fail_free_ai)

    answer = app.ask_no_key_assistant(exam, "what is the syllabus")

    assert "Main syllabus areas" in answer
    assert "Physics" in answer


def test_adk_tools_find_exam_details_and_build_plan():
    search = adk_tools.find_exams("jee", limit=2)
    details = adk_tools.get_exam_details("JEE Main")
    plan = adk_tools.build_study_plan("JEE Main", "Make a 30-day preparation plan.", 30)

    assert search["status"] == "success"
    assert search["exams"][0]["name"] == "Joint Entrance Examination (JEE Main)"
    assert details["status"] == "success"
    assert "books" in details["exam"]
    assert plan["status"] == "success"
    assert "30-day structure" in plan["plan"]


def test_adk_tools_save_and_recall_student_memory(tmp_path, monkeypatch):
    monkeypatch.setattr(adk_tools, "MEMORY_DIR", tmp_path)

    saved = adk_tools.save_student_memory(
        "Student 1",
        target_exam="GATE",
        goal="Revise engineering mathematics",
        weak_topics="Aptitude",
    )
    recalled = adk_tools.recall_student_memory("student-1")

    assert saved["status"] == "success"
    assert saved["student_id"] == "student-1"
    assert recalled["memory"]["target_exam"] == "GATE"
    assert recalled["memory"]["weak_topics"] == "Aptitude"


def test_default_groq_model_uses_official_quickstart_model():
    assert app.DEFAULT_BYOK_MODEL == "llama-3.3-70b-versatile"


def test_ask_openai_compatible_sends_groq_chat_payload(monkeypatch):
    captured = {}

    def fake_post_json(url, payload, headers=None, timeout=45):
        captured["url"] = url
        captured["payload"] = payload
        captured["headers"] = headers
        return {"choices": [{"message": {"content": "AI answer"}}]}

    monkeypatch.setattr(app, "post_json", fake_post_json)

    answer = app.ask_openai_compatible(app.DEFAULT_BYOK_URL, "secret", "llama-3.3-70b-versatile", "prompt")

    assert answer == "AI answer"
    assert captured["url"] == app.DEFAULT_BYOK_URL
    assert captured["payload"]["model"] == "llama-3.3-70b-versatile"
    assert captured["payload"]["max_completion_tokens"] == 700
    assert captured["headers"] == {"Authorization": "Bearer secret"}


def test_ask_openai_compatible_strips_copied_api_key_whitespace(monkeypatch):
    captured = {}

    def fake_post_json(url, payload, headers=None, timeout=45):
        captured["headers"] = headers
        return {"choices": [{"message": {"content": "AI answer"}}]}

    monkeypatch.setattr(app, "post_json", fake_post_json)

    app.ask_openai_compatible(app.DEFAULT_BYOK_URL, "  secret-key\r\n", "llama-3.3-70b-versatile", "prompt")

    assert captured["headers"] == {"Authorization": "Bearer secret-key"}


def test_groq_auto_model_tries_official_model_before_available_model_list(monkeypatch):
    calls = []

    monkeypatch.setattr(app, "get_openai_compatible_models", lambda endpoint, token: ["model-from-account"])

    def fake_openai_compatible(endpoint, token, model, prompt):
        calls.append((endpoint, token, model, prompt))
        return "answer"

    monkeypatch.setattr(app, "ask_openai_compatible", fake_openai_compatible)

    answer = app.ask_groq_with_fallback("token", "auto", "prompt")

    assert answer == "answer"
    assert calls == [(app.DEFAULT_BYOK_URL, "token", "llama-3.3-70b-versatile", "prompt")]


def test_groq_retries_error_1010_with_next_available_model(monkeypatch):
    calls = []

    monkeypatch.setattr(app, "get_openai_compatible_models", lambda endpoint, token: ["working-model"])

    def fake_openai_compatible(endpoint, token, model, prompt):
        calls.append(model)
        if model in app.GROQ_FALLBACK_MODELS:
            raise HTTPError(endpoint, 403, "Forbidden", {}, BytesIO(b'{"error":{"message":"error code: 1010"}}'))
        return "answer"

    monkeypatch.setattr(app, "ask_openai_compatible", fake_openai_compatible)

    answer = app.ask_groq_with_fallback("token", "auto", "prompt")

    assert answer == "answer"
    assert calls == [*app.GROQ_FALLBACK_MODELS, "working-model"]


def test_local_study_response_returns_plan_without_provider():
    exam = app.load_exams()[0]

    response = app.build_local_study_response(exam, "Make a 30-day preparation plan.")

    assert "30-day structure" in response
    assert exam["name"] in response
    assert "Verify dates" in response


def test_local_study_response_answers_exam_use_question():
    exam = next(item for item in app.load_exams() if "GATE" in item["name"])

    response = app.build_local_study_response(exam, "what is the use of this exam")

    assert "Graduate Aptitude Test in Engineering (GATE) is used for" in response
    assert "M.Tech admissions" in response
    assert "30-day structure" not in response


def test_local_study_response_answers_useful_for_engineering_question():
    exam = app.load_exams()[0]

    response = app.build_local_study_response(exam, "is this useful exam for engineering")

    assert "Yes. Joint Entrance Examination (JEE Main) is useful for engineering students." in response
    assert "Admission to NITs, IIITs, GFTIs" in response
    assert "30-day structure" not in response


def test_local_study_response_answers_syllabus_question():
    exam = app.load_exams()[0]

    response = app.build_local_study_response(exam, "what is the syllabus")

    assert "Main syllabus areas" in response
    assert "Physics" in response
    assert "30-day structure" not in response


def test_diagnose_groq_access_reports_working_chat_model(monkeypatch):
    monkeypatch.setattr(app, "get_openai_compatible_models", lambda endpoint, token: ["working-model"])
    monkeypatch.setattr(app, "ask_openai_compatible", lambda endpoint, token, model, prompt: "OK")

    diagnosis = app.diagnose_groq_access("token", "auto")

    assert diagnosis["ok"] is True
    assert diagnosis["model"] == "working-model"
    assert diagnosis["models"] == ["working-model"]
    assert "/chat/completions both worked" in diagnosis["message"]


def test_diagnose_groq_access_reports_chat_permission_failure(monkeypatch):
    monkeypatch.setattr(app, "get_openai_compatible_models", lambda endpoint, token: ["blocked-model"])

    def fail_chat(endpoint, token, model, prompt):
        raise HTTPError(endpoint, 403, "Forbidden", {}, BytesIO(b'{"error":{"message":"error code: 1010"}}'))

    monkeypatch.setattr(app, "ask_openai_compatible", fail_chat)

    diagnosis = app.diagnose_groq_access("token", "auto")

    assert diagnosis["ok"] is False
    assert diagnosis["models"] == ["blocked-model"]
    assert "/models worked" in diagnosis["message"]
    assert "1010" not in diagnosis["message"]


def test_format_ai_error_hides_provider_detail_for_forbidden_response():
    exc = HTTPError(
        app.DEFAULT_BYOK_URL,
        403,
        "Forbidden",
        {},
        BytesIO(b'{"error":{"message":"The selected model is not enabled for this project."}}'),
    )

    message = app.format_ai_error(app.AI_PROVIDER_BYOK, app.DEFAULT_BYOK_URL, exc)

    assert "Groq API request failed" in message
    assert "No local answer was used" in message
    assert "selected model is not enabled" not in message


def test_format_ai_error_explains_ollama_address_failure():
    message = app.format_ai_error(
        app.AI_PROVIDER_OLLAMA,
        app.DEFAULT_OLLAMA_URL,
        OSError("[Errno 99] Cannot assign requested address"),
    )

    assert "Could not connect to Ollama" in message
    assert "ollama run llama3.2" in message
