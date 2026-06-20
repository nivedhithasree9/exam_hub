from json import JSONDecodeError, dumps, loads
from pathlib import Path

import app

MEMORY_DIR = Path(__file__).resolve().parent / ".adk_memory"


def _safe_memory_key(student_id: str) -> str:
    student_id = student_id if isinstance(student_id, str) else ""
    key = "".join(ch.lower() if ch.isalnum() else "-" for ch in student_id.strip()).strip("-")
    return key or "default-student"


def _memory_path(student_id: str) -> Path:
    return MEMORY_DIR / f"{_safe_memory_key(student_id)}.json"


def _exam_summary(exam: dict) -> dict:
    return {
        "name": exam["name"],
        "category": exam["category"],
        "description": exam["description"],
        "eligibility": exam["eligibility"],
        "pattern": exam["pattern"],
        "syllabus": exam["syllabus"],
        "dates": exam["dates"],
        "officialWebsite": exam.get("officialWebsite", ""),
    }


def find_exams(query: str = "", category: str = "All categories", limit: int = 5) -> dict:
    """Find matching exams from Exam Hub by query and category."""
    exams = app.load_exams()
    query = query.strip() if isinstance(query, str) else ""
    category_filter = category.strip() if isinstance(category, str) else "All categories"
    category_filter = category_filter or "All categories"
    matches = [
        _exam_summary(exam)
        for exam in exams
        if app.matches_filters(exam, query, category_filter)
    ]
    try:
        limit = int(limit or 5)
    except (TypeError, ValueError):
        limit = 5
    limit = max(1, min(limit, 10))
    return {
        "status": "success",
        "count": len(matches),
        "exams": matches[:limit],
    }


def get_exam_details(exam_name: str) -> dict:
    """Return detailed structured information for one exam."""
    query = exam_name.strip() if isinstance(exam_name, str) else ""
    if not query:
        return {"status": "error", "message": "exam_name is required."}

    matches = [exam for exam in app.load_exams() if app.matches_filters(exam, query, "All categories")]
    if not matches:
        return {"status": "not_found", "message": f"No exam matched {exam_name!r}."}

    exam = matches[0]
    return {
        "status": "success",
        "exam": {
            **_exam_summary(exam),
            "conductedBy": exam.get("conductedBy", "Check official notice"),
            "duration": exam.get("duration", "Check official notice"),
            "useFor": exam.get("useFor", "Check official notice"),
            "selectionProcess": exam.get("selectionProcess", []),
            "books": exam.get("books", []),
            "preparationTips": exam.get("preparationTips", []),
            "applicationSteps": exam.get("applicationSteps", []),
            "pyq": exam.get("pyq", []),
        },
    }


def build_study_plan(exam_name: str, student_goal: str = "", days: int = 30) -> dict:
    """Build a practical exam preparation plan using Exam Hub data."""
    details = get_exam_details(exam_name)
    if details["status"] != "success":
        return details

    exam = next(exam for exam in app.load_exams() if exam["name"] == details["exam"]["name"])
    goal = student_goal.strip() if isinstance(student_goal, str) else ""
    goal = goal or f"Make a {days}-day preparation plan."
    response = app.build_local_study_response(exam, goal)
    return {
        "status": "success",
        "exam": exam["name"],
        "days": days,
        "plan": response,
    }


def save_student_memory(
    student_id: str,
    target_exam: str = "",
    goal: str = "",
    weak_topics: str = "",
    available_time: str = "",
) -> dict:
    """Save a student's preparation preferences for later agent turns."""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    path = _memory_path(student_id)
    memory = {}
    if path.exists():
        try:
            memory = loads(path.read_text(encoding="utf-8"))
        except (JSONDecodeError, OSError):
            memory = {}

    updates = {
        "target_exam": target_exam.strip() if isinstance(target_exam, str) else "",
        "goal": goal.strip() if isinstance(goal, str) else "",
        "weak_topics": weak_topics.strip() if isinstance(weak_topics, str) else "",
        "available_time": available_time.strip() if isinstance(available_time, str) else "",
    }
    memory.update({key: value for key, value in updates.items() if value})
    path.write_text(dumps(memory, indent=2, sort_keys=True), encoding="utf-8")
    return {"status": "success", "student_id": _safe_memory_key(student_id), "memory": memory}


def recall_student_memory(student_id: str) -> dict:
    """Recall saved preparation preferences for a student."""
    path = _memory_path(student_id)
    if not path.exists():
        return {"status": "empty", "student_id": _safe_memory_key(student_id), "memory": {}}

    try:
        memory = loads(path.read_text(encoding="utf-8"))
    except (JSONDecodeError, OSError) as exc:
        return {"status": "error", "message": f"Could not read saved memory: {exc}"}
    return {"status": "success", "student_id": _safe_memory_key(student_id), "memory": memory}
