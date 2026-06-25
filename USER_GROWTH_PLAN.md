# Exam Hub User Growth Plan

## Purpose

This plan outlines how Exam Hub can reach more students, keep them engaged, and
turn usage feedback into product improvements.

## Target Users

- Students preparing for Indian competitive exams.
- Parents and mentors helping students compare exam options.
- Teachers, coaching centers, and campus placement or career guidance teams.
- First-time applicants who need clear eligibility, syllabus, and deadline
  information before reading official notifications.

## Growth Goals

1. Increase first-time visits from students searching for exam information.
2. Improve return usage by making exam comparison and study guidance useful.
3. Build trust by keeping data, official links, and safety guidance visible.
4. Convert user questions into better exam coverage and app features.

## Acquisition Channels

- Share exam category pages and screenshots with student groups, colleges, and
  career guidance communities.
- Publish short comparison posts for popular exams such as JEE, NEET, UPSC,
  SSC, banking, teaching, law, and management exams.
- Create simple walkthrough videos showing search, filters, exam details, and
  AI study guidance.
- Encourage contributors to add missing exams, improve translations, and verify
  official links.
- Use GitLab/GitHub project documentation to attract open-source contributors.

## Activation

New users should quickly understand the app value. The first session should help
them:

- Search for an exam by name or goal.
- Filter exams by category.
- Open a detail view and find eligibility, syllabus, pattern, dates, fees,
  official links, and preparation tips.
- Generate a study plan with the AI Assistant.
- Verify important details on the official exam website.

## Retention

- Keep exam content current and mark uncertain dates clearly.
- Add more regional-language labels and exam summaries.
- Improve saved study goals and lightweight student memory in the ADK agent.
- Maintain fast search and predictable filters.
- Review user feedback regularly and turn common questions into data updates.

## Trust And Safety

- Do not collect secrets or private student data in the repository.
- Keep `.env.example` limited to placeholder values.
- Remind users to verify deadlines, fees, eligibility, and official notices.
- Keep quality, security, type-checking, and test automation passing in CI.
- Document known limitations clearly in the README and user manual.

## Metrics

Track these indicators when deployment analytics are available:

- Number of unique visitors.
- Number of returning users.
- Search queries with no results.
- Most viewed exam categories.
- AI Assistant usage count.
- Official-link click-through rate.
- User feedback items opened and resolved.
- Contribution count for exam data, translations, tests, and documentation.

## 90-Day Roadmap

### Days 1-30

- Validate that all current exam entries have official links.
- Add missing high-demand exams from student feedback.
- Publish basic usage screenshots or a short demo video.
- Confirm CI, secret scanning, dependency audit, tests, and coverage stay green.

### Days 31-60

- Improve category coverage and search synonyms.
- Add more Telugu and other regional-language content where useful.
- Add feedback prompts or issue templates for missing exams and incorrect data.
- Improve AI study prompts for exam-specific study plans.

### Days 61-90

- Review analytics and prioritize the top missing searches.
- Add comparison-focused documentation for major exam groups.
- Improve onboarding copy in docs and deployment instructions.
- Create a release note summarizing new exams, fixes, and quality improvements.

## Feedback Loop

1. Collect student questions, missing exams, and outdated-data reports.
2. Triage feedback by exam popularity, urgency, and reliability of sources.
3. Update data and tests together.
4. Verify official links and safety notes.
5. Document changes in `CHANGELOG.md` or release notes.

## Success Criteria

Exam Hub growth is healthy when students can find relevant exams quickly, trust
the source links, return for planning help, and contributors can safely improve
the project without weakening quality or compliance.
