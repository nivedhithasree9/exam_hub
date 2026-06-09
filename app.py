from copy import deepcopy
from urllib.parse import quote_plus

import streamlit as st


def make_pyqs(prefix):
    slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in prefix).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")

    papers = []
    for index in range(2):
        year = 2025 - index
        query = quote_plus(f"{prefix} {year} previous year question paper pdf")
        papers.append(
            {
                "year": year,
                "title": f"{prefix} {year}",
                "url": f"https://www.google.com/search?q={query}",
                "file": f"/papers/{slug}-{year}.pdf",
            }
        )
    return papers


APPLICATION_STEPS = [
    "Visit the official exam website and open the latest notification.",
    "Create an account or sign in with your registered email/mobile number.",
    "Fill personal, educational, category, and exam-city details carefully.",
    "Upload photograph, signature, and required certificates in the specified format.",
    "Pay the application fee if applicable and save the payment receipt.",
    "Download the submitted application form and keep it for future reference.",
]


BASE_EXAMS = [
    {
        "name": "Joint Entrance Examination (JEE Main)",
        "category": "Engineering",
        "description": "Entrance exam for NITs, IIITs, GFTIs, and JEE Advanced qualification.",
        "eligibility": "Passed or appearing in 10+2 with Physics, Chemistry, and Mathematics.",
        "syllabus": ["Physics", "Chemistry", "Mathematics"],
        "pattern": "Computer-based test with MCQs and numerical value questions.",
        "books": [
            "Physics: Concepts of Physics Vol. 1 & 2 - H.C. Verma",
            "Chemistry: NCERT Class 11 & 12 Chemistry",
            "Mathematics: Objective Mathematics for JEE - R.D. Sharma",
            "Practice: Arihant JEE Main Previous Years Solved Papers",
        ],
        "dates": {"notification": "November", "examDate": "January / April"},
        "conductedBy": "National Testing Agency (NTA)",
        "frequency": "Usually twice a year",
        "applicationMode": "Online",
        "examMode": "Computer-based test",
        "duration": "3 hours",
        "fee": "Varies by category, paper, and exam city",
        "officialWebsite": "https://jeemain.nta.nic.in",
        "useFor": "Admission to NITs, IIITs, GFTIs, and eligibility for JEE Advanced.",
        "selectionProcess": [
            "Apply online",
            "Appear for JEE Main",
            "Use score for NIT/IIIT/GFTI admission",
            "Top candidates qualify for JEE Advanced",
        ],
        "preparationTips": [
            "Master NCERT Chemistry",
            "Practice numerical problems daily",
            "Analyze mock test mistakes",
            "Revise formulas frequently",
        ],
    },
    {
        "name": "Joint Entrance Examination (JEE Advanced)",
        "category": "Engineering",
        "description": "National level engineering entrance exam for IIT admissions.",
        "eligibility": "Qualified JEE Main and passed 10+2 with Physics, Chemistry, and Mathematics.",
        "syllabus": ["Physics", "Chemistry", "Mathematics"],
        "pattern": "Two computer-based papers with numerical and objective questions.",
        "books": [
            "Physics: Concepts of Physics Vol. 1 & 2 - H.C. Verma",
            "Physics: Problems in General Physics - I.E. Irodov",
            "Chemistry: NCERT Class 11 & 12 Chemistry",
            "Mathematics: Cengage JEE Advanced Mathematics series",
        ],
        "dates": {"notification": "April", "examDate": "June"},
        "conductedBy": "One of the IITs on a rotating basis under JAB",
        "frequency": "Once a year",
        "applicationMode": "Online",
        "examMode": "Computer-based test",
        "duration": "Two papers of 3 hours each",
        "fee": "Varies by category and nationality",
        "officialWebsite": "https://jeeadv.ac.in",
        "useFor": "Admission to IIT undergraduate engineering and science programs.",
        "selectionProcess": [
            "Qualify JEE Main",
            "Register for JEE Advanced",
            "Appear for both papers",
            "Participate in JoSAA counselling",
        ],
        "preparationTips": [
            "Revise JEE Main concepts deeply",
            "Practice mixed-subject problems",
            "Solve previous IIT papers",
            "Take full-length mock tests",
        ],
    },
    {
        "name": "National Eligibility cum Entrance Test (NEET UG)",
        "category": "Medical",
        "description": "Medical entrance exam for MBBS, BDS, and allied undergraduate courses.",
        "eligibility": "10+2 with Physics, Chemistry, Biology/Biotechnology, and English.",
        "syllabus": ["Physics", "Chemistry", "Botany", "Zoology"],
        "pattern": "Offline objective exam based on NCERT syllabus.",
        "books": [
            "Biology: NCERT Class 11 & 12 Biology",
            "Biology Practice: MTG Objective NCERT at Your Fingertips",
            "Physics: Concepts of Physics - H.C. Verma",
            "Chemistry: NCERT Chemistry with MTG/Arihant practice questions",
        ],
        "dates": {"notification": "February", "examDate": "May"},
        "conductedBy": "National Testing Agency (NTA)",
        "frequency": "Once a year",
        "applicationMode": "Online",
        "examMode": "Offline pen-and-paper test",
        "duration": "3 hours 20 minutes",
        "fee": "Varies by category and exam center location",
        "officialWebsite": "https://neet.nta.nic.in",
        "useFor": "Admission to MBBS, BDS, AYUSH, and other medical programs.",
        "selectionProcess": [
            "Apply online",
            "Appear for NEET UG",
            "Check rank and score",
            "Participate in medical counselling",
        ],
        "preparationTips": [
            "Read NCERT Biology line by line",
            "Practice Physics numericals",
            "Revise reactions and formulas",
            "Attempt timed mock tests",
        ],
    },
    {
        "name": "Graduate Aptitude Test in Engineering (GATE)",
        "category": "Engineering",
        "description": "Postgraduate engineering entrance and PSU recruitment exam.",
        "eligibility": "Engineering, science, architecture, or relevant degree students/graduates.",
        "syllabus": ["Core engineering subject", "Engineering Mathematics", "General Aptitude"],
        "pattern": "Computer-based test with MCQ, MSQ, and numerical answer questions.",
        "books": [
            "Core Subject: Made Easy GATE study package",
            "Core Subject: ACE Academy GATE material",
            "Engineering Mathematics: Made Easy Engineering Mathematics",
            "Practice: GATE previous year solved papers by Made Easy/Ace Academy",
        ],
        "dates": {"notification": "August", "examDate": "February"},
        "conductedBy": "IISc/IITs on a rotating basis",
        "frequency": "Once a year",
        "applicationMode": "Online",
        "examMode": "Computer-based test",
        "duration": "3 hours",
        "fee": "Varies by category and application timing",
        "officialWebsite": "https://gate2026.iitg.ac.in",
        "useFor": "M.Tech admissions, research programs, and PSU recruitment.",
        "selectionProcess": [
            "Apply for selected paper",
            "Appear for GATE",
            "Use score for M.Tech/PhD admissions or PSU applications",
        ],
        "preparationTips": [
            "Finish core subjects first",
            "Revise Engineering Mathematics",
            "Practice previous papers",
            "Make short revision notes",
        ],
    },
    {
        "name": "Common Admission Test (CAT)",
        "category": "Management",
        "description": "MBA entrance exam for IIMs and other business schools.",
        "eligibility": "Bachelor degree with required minimum marks.",
        "syllabus": ["VARC", "DILR", "Quantitative Aptitude"],
        "pattern": "Computer-based test with sectional time limits.",
        "books": [
            "Quantitative Aptitude: How to Prepare for Quantitative Aptitude - Arun Sharma",
            "DILR: How to Prepare for Data Interpretation & Logical Reasoning - Arun Sharma",
            "VARC: Word Power Made Easy - Norman Lewis",
            "Practice: CAT previous year papers and IMS/TIME/CL mock tests",
        ],
        "dates": {"notification": "July", "examDate": "November"},
        "conductedBy": "Indian Institutes of Management (IIMs)",
        "frequency": "Once a year",
        "applicationMode": "Online",
        "examMode": "Computer-based test",
        "duration": "About 2 hours",
        "fee": "Varies by category",
        "officialWebsite": "https://iimcat.ac.in",
        "useFor": "MBA/PGDM admission to IIMs and many business schools.",
        "selectionProcess": [
            "Register for CAT",
            "Appear for exam",
            "Shortlisting by institutes",
            "WAT/GD/PI or interview rounds",
        ],
        "preparationTips": [
            "Read daily for VARC",
            "Practice DILR sets",
            "Build arithmetic speed",
            "Take sectional mocks",
        ],
    },
    {
        "name": "Union Public Service Commission (UPSC) CSE",
        "category": "Government",
        "description": "Civil services exam for IAS, IPS, IFS, and allied services.",
        "eligibility": "Graduation from a recognized university.",
        "syllabus": ["General Studies", "CSAT", "Optional subject", "Essay"],
        "pattern": "Prelims, Mains, and Interview.",
        "books": [
            "Polity: Indian Polity - M. Laxmikanth",
            "Geography: Certificate Physical and Human Geography - G.C. Leong",
            "History: Spectrum Modern India - Rajiv Ahir",
            "Economy: Indian Economy - Ramesh Singh",
        ],
        "dates": {"notification": "February", "examDate": "May"},
        "conductedBy": "Union Public Service Commission",
        "frequency": "Once a year",
        "applicationMode": "Online",
        "examMode": "Offline written exam and interview",
        "duration": "Multiple papers across Prelims and Mains",
        "fee": "Varies by category; many categories are exempt",
        "officialWebsite": "https://upsc.gov.in",
        "useFor": "Recruitment to IAS, IPS, IFS, IRS, and other central services.",
        "selectionProcess": ["Preliminary exam", "Main examination", "Personality test", "Final merit list"],
        "preparationTips": [
            "Read NCERTs and standard books",
            "Follow current affairs",
            "Practice answer writing",
            "Revise syllabus repeatedly",
        ],
    },
    {
        "name": "Staff Selection Commission (SSC) CGL",
        "category": "Government",
        "description": "Graduate level recruitment for central government ministries and departments.",
        "eligibility": "Graduation from a recognized university.",
        "syllabus": ["Quantitative Aptitude", "Reasoning", "English", "General Awareness"],
        "pattern": "Tiered computer-based examinations.",
        "books": [
            "Quantitative Aptitude: R.S. Aggarwal or Kiran SSC Maths",
            "Reasoning: A Modern Approach to Verbal & Non-Verbal Reasoning - R.S. Aggarwal",
            "English: Objective General English - S.P. Bakshi",
            "General Awareness: Lucent General Knowledge",
        ],
        "dates": {"notification": "June", "examDate": "September"},
        "conductedBy": "Staff Selection Commission",
        "frequency": "Once a year",
        "applicationMode": "Online",
        "examMode": "Computer-based test",
        "duration": "Varies by tier",
        "fee": "Varies by category; many categories are exempt",
        "officialWebsite": "https://ssc.gov.in",
        "useFor": "Central government Group B and Group C posts.",
        "selectionProcess": ["Tier I", "Tier II", "Document verification", "Final allocation"],
        "preparationTips": [
            "Practice arithmetic daily",
            "Revise current affairs",
            "Improve English grammar",
            "Solve previous SSC papers",
        ],
    },
    {
        "name": "Institute of Banking Personnel Selection PO (IBPS PO)",
        "category": "Banking",
        "description": "Probationary Officer recruitment exam for public sector banks.",
        "eligibility": "Graduation from a recognized university.",
        "syllabus": ["Reasoning", "Quantitative Aptitude", "English", "Banking Awareness"],
        "pattern": "Prelims, Mains, and Interview.",
        "books": [
            "Banking Awareness: Arihant Banking Awareness",
            "Quantitative Aptitude: Fast Track Objective Arithmetic - Rajesh Verma",
            "Reasoning: A Modern Approach to Verbal & Non-Verbal Reasoning - R.S. Aggarwal",
            "English: Word Power Made Easy - Norman Lewis",
        ],
        "dates": {"notification": "August", "examDate": "October"},
        "conductedBy": "Institute of Banking Personnel Selection",
        "frequency": "Once a year",
        "applicationMode": "Online",
        "examMode": "Computer-based test",
        "duration": "Prelims and Mains have separate durations",
        "fee": "Varies by category",
        "officialWebsite": "https://www.ibps.in",
        "useFor": "Probationary Officer recruitment in public sector banks.",
        "selectionProcess": ["Preliminary exam", "Main exam", "Interview", "Provisional allotment"],
        "preparationTips": [
            "Practice speed maths",
            "Read banking awareness",
            "Solve puzzles daily",
            "Improve reading comprehension",
        ],
    },
    {
        "name": "Common Law Admission Test (CLAT)",
        "category": "Law",
        "description": "Entrance exam for undergraduate and postgraduate law programs at NLUs.",
        "eligibility": "10+2 for UG law programs; LLB for PG law programs.",
        "syllabus": [
            "English",
            "Current Affairs",
            "Legal Reasoning",
            "Logical Reasoning",
            "Quantitative Techniques",
        ],
        "pattern": "Offline comprehension-based objective test.",
        "books": [
            "Legal Reasoning: Legal Awareness and Legal Reasoning - A.P. Bhardwaj",
            "English: Word Power Made Easy - Norman Lewis",
            "Current Affairs: Manorama Yearbook plus monthly current affairs",
            "Practice: Universal/LexisNexis CLAT previous year papers",
        ],
        "dates": {"notification": "July", "examDate": "December"},
        "conductedBy": "Consortium of National Law Universities",
        "frequency": "Once a year",
        "applicationMode": "Online",
        "examMode": "Offline pen-and-paper test",
        "duration": "2 hours",
        "fee": "Varies by category",
        "officialWebsite": "https://consortiumofnlus.ac.in",
        "useFor": "Admission to law programs at National Law Universities.",
        "selectionProcess": ["Apply online", "Appear for CLAT", "Check rank", "Participate in NLU counselling"],
        "preparationTips": [
            "Read editorials daily",
            "Practice legal reasoning passages",
            "Revise current affairs",
            "Solve mock papers",
        ],
    },
]


@st.cache_data
def load_exams():
    exams = []
    for index, exam in enumerate(BASE_EXAMS, start=1):
        item = deepcopy(exam)
        short_name = item["name"].split("(")[0].strip()
        item["id"] = index
        item["pyq"] = make_pyqs(short_name)
        item["applicationSteps"] = APPLICATION_STEPS
        exams.append(item)
    return exams


def matches_filters(exam, query, category):
    query_matches = not query or query in exam["name"].lower() or query in exam["description"].lower()
    category_matches = category == "All categories" or exam["category"] == category
    return query_matches and category_matches


def render_exam_details(exam):
    st.subheader(exam["name"])
    st.caption(exam["category"])
    st.write(exam["description"])

    facts = [
        ("Conducted by", exam.get("conductedBy")),
        ("Frequency", exam.get("frequency")),
        ("Exam mode", exam.get("examMode")),
        ("Duration", exam.get("duration")),
    ]
    fact_cols = st.columns(4)
    for column, (label, value) in zip(fact_cols, facts):
        column.metric(label, value or "Check notice")

    overview_tab, syllabus_tab, prep_tab, apply_tab = st.tabs(
        ["Overview", "Syllabus", "Preparation", "Apply"]
    )

    with overview_tab:
        st.markdown("**Eligibility**")
        st.write(exam["eligibility"])
        st.markdown("**Exam pattern**")
        st.write(exam["pattern"])
        st.markdown("**Used for**")
        st.write(exam["useFor"])
        st.markdown("**Important dates**")
        st.table(
            {
                "Stage": ["Notification", "Exam date"],
                "Timeline": [
                    exam["dates"].get("notification", "To be announced"),
                    exam["dates"].get("examDate", "To be announced"),
                ],
            }
        )

    with syllabus_tab:
        for item in exam["syllabus"]:
            st.markdown(f"- {item}")
        st.markdown("**Selection process**")
        for index, step in enumerate(exam["selectionProcess"], start=1):
            st.write(f"{index}. {step}")

    with prep_tab:
        st.markdown("**Recommended books and study material**")
        for book in exam["books"]:
            st.markdown(f"- {book}")
        st.markdown("**Preparation tips**")
        for tip in exam["preparationTips"]:
            st.markdown(f"- {tip}")
        st.markdown("**Previous year question papers**")
        for paper in exam["pyq"]:
            st.link_button(f"{paper['year']} Question Paper", paper["url"])

    with apply_tab:
        st.markdown("**Application mode**")
        st.write(exam.get("applicationMode", "Check latest notification"))
        st.markdown("**Fee**")
        st.write(exam.get("fee", "Check latest notification"))
        if exam.get("officialWebsite"):
            st.link_button("Open official website", exam["officialWebsite"])
        st.markdown("**How to apply**")
        for index, step in enumerate(exam["applicationSteps"], start=1):
            st.write(f"{index}. {step}")


def main():
    st.set_page_config(page_title="Exam Hub", page_icon="EH", layout="wide")

    st.title("Exam Hub")
    st.write("Search, compare, and prepare for major Indian competitive exams.")

    exams = load_exams()
    categories = ["All categories"] + sorted({exam["category"] for exam in exams})

    with st.sidebar:
        st.header("Filters")
        query = st.text_input("Search exams", placeholder="NEET, UPSC, JEE").strip().lower()
        category = st.selectbox("Category", categories)
        st.metric("Total exams", len(exams))
        st.metric("Categories", len(categories) - 1)

    filtered_exams = [exam for exam in exams if matches_filters(exam, query, category)]

    st.caption(f"{len(filtered_exams)} result{'s' if len(filtered_exams) != 1 else ''}")
    if not filtered_exams:
        st.info("No exams found. Try a different search term or category.")
        return

    exam_names = [exam["name"] for exam in filtered_exams]
    selected_name = st.selectbox("Choose an exam", exam_names)
    selected_exam = next(exam for exam in filtered_exams if exam["name"] == selected_name)

    render_exam_details(selected_exam)


if __name__ == "__main__":
    main()
