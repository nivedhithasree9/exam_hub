from os import getenv

try:
    from google.adk.agents.llm_agent import Agent
except ImportError:  # pragma: no cover
    from google.adk import Agent

from .tools import (
    build_study_plan,
    find_exams,
    get_exam_details,
    recall_student_memory,
    save_student_memory,
)

AGENT_MODEL = getenv("EXAM_HUB_ADK_MODEL", "gemini-flash-latest")

root_agent = Agent(
    model=AGENT_MODEL,
    name="exam_hub_agent",
    description="Autonomous exam preparation mentor for Indian competitive exams.",
    instruction=(
        "You are Exam Hub's autonomous study mentor. Help students compare exams, "
        "understand eligibility, build preparation plans, and remember their stated "
        "exam goals. Use the provided tools before answering questions about exam "
        "facts, syllabus, books, previous papers, or saved student preferences. "
        "When dates, fees, eligibility, or reservation rules may change, tell the "
        "student to verify the latest official notification. Keep answers concise, "
        "practical, and student-friendly."
    ),
    tools=[
        find_exams,
        get_exam_details,
        build_study_plan,
        save_student_memory,
        recall_student_memory,
    ],
)
