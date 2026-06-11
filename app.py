from copy import deepcopy
from html import escape
from json import JSONDecodeError, loads
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlencode
from urllib.request import urlopen

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


def make_book_links(book):
    query = quote_plus(book)
    return {
        "Amazon": f"https://www.amazon.in/s?k={query}",
        "Flipkart": f"https://www.flipkart.com/search?q={query}",
    }


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
        "syllabus": [
            "Core engineering subject",
            "Engineering Mathematics",
            "General Aptitude",
        ],
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
        "selectionProcess": [
            "Preliminary exam",
            "Main examination",
            "Personality test",
            "Final merit list",
        ],
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
        "syllabus": [
            "Quantitative Aptitude",
            "Reasoning",
            "English",
            "General Awareness",
        ],
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
        "selectionProcess": [
            "Tier I",
            "Tier II",
            "Document verification",
            "Final allocation",
        ],
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
        "syllabus": [
            "Reasoning",
            "Quantitative Aptitude",
            "English",
            "Banking Awareness",
        ],
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
        "selectionProcess": [
            "Preliminary exam",
            "Main exam",
            "Interview",
            "Provisional allotment",
        ],
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
        "selectionProcess": [
            "Apply online",
            "Appear for CLAT",
            "Check rank",
            "Participate in NLU counselling",
        ],
        "preparationTips": [
            "Read editorials daily",
            "Practice legal reasoning passages",
            "Revise current affairs",
            "Solve mock papers",
        ],
    },
]


def exam_record(
    name,
    category,
    description,
    eligibility,
    syllabus,
    pattern,
    conducted_by,
    official_website,
    use_for,
    selection_process,
    notification="As per official calendar",
    exam_date="As per official calendar",
    duration="Check latest notification",
    exam_mode="Check latest notification",
    frequency="Usually once a year",
    books=None,
    tips=None,
):
    return {
        "name": name,
        "category": category,
        "description": description,
        "eligibility": eligibility,
        "syllabus": syllabus,
        "pattern": pattern,
        "books": books
        or [
            "Official syllabus and latest notification",
            "NCERT/standard textbooks for foundation concepts",
            "Previous year papers and full-length mock tests",
            "A trusted current affairs source where applicable",
        ],
        "dates": {"notification": notification, "examDate": exam_date},
        "conductedBy": conducted_by,
        "frequency": frequency,
        "applicationMode": "Online",
        "examMode": exam_mode,
        "duration": duration,
        "fee": "Varies by category and notification",
        "officialWebsite": official_website,
        "useFor": use_for,
        "selectionProcess": selection_process,
        "preparationTips": tips
        or [
            "Start from the official syllabus and exam pattern",
            "Solve topic-wise questions before full mocks",
            "Revise weak areas every week",
            "Read the latest notification before applying",
        ],
    }


ADDITIONAL_EXAMS = [
    exam_record(
        "Common University Entrance Test (CUET UG)",
        "University",
        "National entrance exam for undergraduate admission in participating universities.",
        "Usually 10+2 passed or appearing; subject rules depend on the university and course.",
        ["Language", "Domain subjects", "General test"],
        "Computer-based test with objective questions across selected subjects.",
        "National Testing Agency (NTA)",
        "https://exams.nta.ac.in/CUET-UG/",
        "UG admission to central, state, deemed, and private participating universities.",
        [
            "Apply with selected subjects",
            "Appear for CUET UG",
            "Download score card",
            "Apply through university portals",
        ],
        "February / March",
        "May / June",
        "Varies by number of subjects",
        "Computer-based test",
    ),
    exam_record(
        "Common University Entrance Test (CUET PG)",
        "University",
        "Entrance exam for postgraduate admission in participating universities.",
        "Bachelor degree or final-year status as required by the selected program.",
        ["Subject knowledge", "General aptitude where applicable"],
        "Computer-based objective exam based on the selected paper code.",
        "National Testing Agency (NTA)",
        "https://exams.nta.ac.in/CUET-PG/",
        "PG admission in participating universities.",
        [
            "Register for paper codes",
            "Appear for CUET PG",
            "Use score in university counselling",
        ],
        "December / January",
        "March / April",
        "Usually 1 hour 45 minutes",
        "Computer-based test",
    ),
    exam_record(
        "BITS Admission Test (BITSAT)",
        "Engineering",
        "Entrance exam for admission to BITS Pilani campuses.",
        "10+2 with Physics, Chemistry, Mathematics/Biology, and English as per program rules.",
        ["Physics", "Chemistry", "Mathematics/Biology", "English", "Logical Reasoning"],
        "Computer-based objective test with bonus questions for eligible candidates.",
        "BITS Pilani",
        "https://www.bitsadmission.com",
        "Admission to undergraduate programs at BITS Pilani, Goa, Hyderabad, and Dubai where applicable.",
        [
            "Apply online",
            "Book test slot",
            "Appear for BITSAT",
            "Submit preference form",
            "Participate in iterations",
        ],
        "January / February",
        "May / June",
        "3 hours",
        "Computer-based test",
    ),
    exam_record(
        "VIT Engineering Entrance Examination (VITEEE)",
        "Engineering",
        "Entrance exam for B.Tech admission at VIT campuses.",
        "10+2 with relevant science subjects as specified by VIT.",
        ["Mathematics/Biology", "Physics", "Chemistry", "English", "Aptitude"],
        "Computer-based objective test.",
        "Vellore Institute of Technology",
        "https://vit.ac.in",
        "B.Tech admission at VIT campuses.",
        ["Apply online", "Appear for VITEEE", "Check rank", "Attend counselling"],
        "November / December",
        "April",
        "2 hours 30 minutes",
        "Computer-based test",
    ),
    exam_record(
        "COMEDK Undergraduate Entrance Test",
        "Engineering",
        "Entrance exam for engineering colleges in Karnataka under COMEDK.",
        "10+2 with Physics, Chemistry, and Mathematics as per notification.",
        ["Physics", "Chemistry", "Mathematics"],
        "Computer-based objective test.",
        "COMEDK",
        "https://www.comedk.org",
        "B.E./B.Tech admission in participating Karnataka private colleges.",
        ["Apply online", "Appear for UGET", "Check rank", "Attend COMEDK counselling"],
        "February",
        "May",
        "3 hours",
        "Computer-based test",
    ),
    exam_record(
        "MHT CET",
        "Engineering",
        "State entrance exam for engineering, pharmacy, and allied courses in Maharashtra.",
        "10+2 with relevant subjects as per Maharashtra CET Cell rules.",
        ["Physics", "Chemistry", "Mathematics/Biology"],
        "Computer-based objective exam based on Maharashtra board syllabus weightage.",
        "Maharashtra State Common Entrance Test Cell",
        "https://cetcell.mahacet.org",
        "Admission to participating colleges in Maharashtra.",
        [
            "Apply online",
            "Appear for CET",
            "Check score",
            "Participate in CAP counselling",
        ],
        "January",
        "April / May",
        "Varies by paper group",
        "Computer-based test",
    ),
    exam_record(
        "KCET",
        "Engineering",
        "Karnataka state entrance exam for engineering, pharmacy, agriculture, and other courses.",
        "10+2 with relevant subjects and domicile/category rules as applicable.",
        ["Physics", "Chemistry", "Mathematics/Biology"],
        "Offline objective papers, with Kannada language test for some candidates.",
        "Karnataka Examinations Authority (KEA)",
        "https://kea.kar.nic.in",
        "Admission to Karnataka professional courses.",
        [
            "Apply online",
            "Appear for KCET",
            "Verify documents",
            "Participate in seat allotment",
        ],
        "January / February",
        "April / May",
        "Varies by subject paper",
        "Offline pen-and-paper test",
    ),
    exam_record(
        "WBJEE",
        "Engineering",
        "West Bengal entrance exam for engineering, technology, pharmacy, and architecture-linked admissions.",
        "10+2 with relevant science subjects as per WBJEEB rules.",
        ["Mathematics", "Physics", "Chemistry"],
        "Offline objective exam in two papers.",
        "West Bengal Joint Entrance Examinations Board",
        "https://wbjeeb.nic.in",
        "Admission to participating institutions in West Bengal.",
        ["Apply online", "Appear for WBJEE", "Check rank", "Attend counselling"],
        "December",
        "April",
        "Two subject papers",
        "Offline pen-and-paper test",
    ),
    exam_record(
        "UGC NET",
        "Teaching",
        "Eligibility test for Assistant Professor and Junior Research Fellowship.",
        "Master degree or equivalent with required marks as per category and subject rules.",
        ["Teaching and research aptitude", "Selected subject"],
        "Two computer-based objective papers conducted in one session.",
        "National Testing Agency (NTA) for UGC",
        "https://ugcnet.nta.ac.in",
        "Assistant Professor eligibility, JRF, and PhD admission use where applicable.",
        [
            "Apply online",
            "Appear for Paper I and II",
            "Check result",
            "Use certificate/score as applicable",
        ],
        "March / September",
        "June / December",
        "3 hours",
        "Computer-based test",
    ),
    exam_record(
        "Central Teacher Eligibility Test (CTET)",
        "Teaching",
        "Teacher eligibility test for Classes I-VIII in central schools and many other institutions.",
        "Teacher education qualification as per Paper I or Paper II requirements.",
        [
            "Child development",
            "Language I",
            "Language II",
            "Mathematics",
            "Environmental Studies / subject pedagogy",
        ],
        "Objective exam with separate papers for primary and upper primary levels.",
        "Central Board of Secondary Education (CBSE)",
        "https://ctet.nic.in",
        "Teacher eligibility for central government schools and accepted institutions.",
        [
            "Apply online",
            "Appear for selected paper",
            "Download certificate after qualifying",
        ],
        "Varies",
        "Usually twice a year",
        "2 hours 30 minutes per paper",
        "Offline or online as notified",
        "Usually twice a year",
    ),
    exam_record(
        "National Defence Academy (NDA) Exam",
        "Defence",
        "UPSC exam for entry into Army, Navy, and Air Force wings of NDA and Naval Academy.",
        "10+2 qualification; PCM required for Air Force/Navy; age and medical standards apply.",
        ["Mathematics", "General Ability Test", "English", "General Knowledge"],
        "Written exam followed by SSB interview and medical examination.",
        "Union Public Service Commission",
        "https://upsc.gov.in",
        "Officer training entry through NDA/NA.",
        [
            "Apply through UPSC",
            "Written exam",
            "SSB interview",
            "Medical test",
            "Final merit",
        ],
        "December / May",
        "April / September",
        "Two written papers",
        "Offline written exam",
        "Twice a year",
    ),
    exam_record(
        "Combined Defence Services (CDS) Exam",
        "Defence",
        "UPSC exam for graduate entry to IMA, INA, AFA, and OTA.",
        "Graduation with service-specific subject requirements, age limits, and medical standards.",
        ["English", "General Knowledge", "Elementary Mathematics"],
        "Written exam followed by SSB interview and medical examination.",
        "Union Public Service Commission",
        "https://upsc.gov.in",
        "Officer entry into Indian armed forces academies.",
        [
            "Apply through UPSC",
            "Written exam",
            "SSB interview",
            "Medical test",
            "Final merit",
        ],
        "December / May",
        "April / September",
        "Varies by academy papers",
        "Offline written exam",
        "Twice a year",
    ),
    exam_record(
        "AFCAT",
        "Defence",
        "Air Force Common Admission Test for officer recruitment in flying and ground duty branches.",
        "Graduation and branch-specific subject/percentage requirements; medical standards apply.",
        [
            "Verbal ability",
            "Numerical ability",
            "Reasoning",
            "General awareness",
            "Military aptitude",
        ],
        "Computer-based exam followed by AFSB selection and medical examination.",
        "Indian Air Force",
        "https://afcat.cdac.in",
        "Commissioned officer entry in Indian Air Force branches.",
        [
            "Apply online",
            "Appear for AFCAT",
            "AFSB interview",
            "Medical examination",
            "Final merit",
        ],
        "June / December",
        "February / August",
        "2 hours",
        "Computer-based test",
        "Twice a year",
    ),
    exam_record(
        "UPSC Engineering Services Examination (ESE)",
        "Government",
        "Engineering services recruitment exam for technical posts under the Government of India.",
        "Engineering degree or equivalent qualification in eligible disciplines.",
        ["Engineering discipline", "Engineering aptitude", "General studies"],
        "Preliminary exam, Main written exam, and personality test.",
        "Union Public Service Commission",
        "https://upsc.gov.in",
        "Recruitment to Indian Engineering Services and allied technical posts.",
        [
            "Preliminary exam",
            "Main exam",
            "Personality test",
            "Medical exam",
            "Final merit",
        ],
        "September",
        "February / June",
        "Multiple papers",
        "Offline written exam",
    ),
    exam_record(
        "UPSC CAPF Assistant Commandant",
        "Government",
        "Recruitment exam for Assistant Commandants in Central Armed Police Forces.",
        "Bachelor degree with age, physical, and medical standards.",
        ["General ability", "General studies", "Essay", "Comprehension"],
        "Written exam followed by physical standards/efficiency test, medical, and interview.",
        "Union Public Service Commission",
        "https://upsc.gov.in",
        "Assistant Commandant recruitment in CAPF forces.",
        [
            "Written exam",
            "Physical tests",
            "Medical examination",
            "Interview",
            "Final merit",
        ],
        "April",
        "August",
        "Two written papers",
        "Offline written exam",
    ),
    exam_record(
        "SSC CHSL",
        "Government",
        "Recruitment exam for 10+2 level central government posts.",
        "Class 12 or equivalent qualification.",
        ["Reasoning", "Quantitative Aptitude", "English", "General Awareness"],
        "Tiered computer-based examination and skill/typing test where applicable.",
        "Staff Selection Commission",
        "https://ssc.gov.in",
        "LDC, JSA, PA/SA, DEO, and related posts.",
        [
            "Tier I",
            "Tier II",
            "Skill/typing test where applicable",
            "Document verification",
        ],
        "April",
        "July / August",
        "Varies by tier",
        "Computer-based test",
    ),
    exam_record(
        "SSC MTS and Havaldar",
        "Government",
        "Recruitment exam for Multi Tasking Staff and Havaldar posts.",
        "Class 10 or equivalent qualification.",
        ["Numerical ability", "Reasoning", "English", "General awareness"],
        "Computer-based exam with physical tests for Havaldar posts.",
        "Staff Selection Commission",
        "https://ssc.gov.in",
        "Central government MTS and Havaldar recruitment.",
        ["Computer-based exam", "PET/PST for Havaldar", "Document verification"],
        "June",
        "September / October",
        "Varies",
        "Computer-based test",
    ),
    exam_record(
        "SSC CPO",
        "Government",
        "Recruitment exam for Sub-Inspector posts in Delhi Police and CAPFs.",
        "Graduation with physical and medical standards; driving license required for some posts.",
        ["Reasoning", "General knowledge", "Quantitative aptitude", "English"],
        "Computer-based exams with physical tests and medical examination.",
        "Staff Selection Commission",
        "https://ssc.gov.in",
        "Sub-Inspector recruitment in Delhi Police and CAPFs.",
        ["Paper I", "PET/PST", "Paper II", "Medical examination", "Final merit"],
        "March",
        "June / July",
        "Varies by paper",
        "Computer-based test",
    ),
    exam_record(
        "RRB NTPC",
        "Railway",
        "Railway recruitment exam for Non-Technical Popular Categories posts.",
        "Class 12 or graduation depending on post.",
        ["General awareness", "Mathematics", "General intelligence and reasoning"],
        "Computer-based stages followed by skill/aptitude test for some posts and document verification.",
        "Railway Recruitment Boards",
        "https://www.rrbcdg.gov.in",
        "Railway clerk, station master, goods train manager, and related posts.",
        [
            "CBT 1",
            "CBT 2",
            "Skill/aptitude test where applicable",
            "Document verification",
            "Medical exam",
        ],
        "As notified by RRB",
        "As notified by RRB",
        "Varies by stage",
        "Computer-based test",
    ),
    exam_record(
        "RRB Group D",
        "Railway",
        "Railway recruitment exam for Level 1 posts.",
        "Class 10 or ITI/equivalent as per post rules.",
        ["General science", "Mathematics", "Reasoning", "General awareness"],
        "Computer-based exam followed by physical efficiency test and document verification.",
        "Railway Recruitment Boards",
        "https://www.rrbcdg.gov.in",
        "Level 1 posts in Indian Railways.",
        ["CBT", "Physical efficiency test", "Document verification", "Medical exam"],
        "As notified by RRB",
        "As notified by RRB",
        "Varies",
        "Computer-based test",
    ),
    exam_record(
        "RRB ALP",
        "Railway",
        "Recruitment exam for Assistant Loco Pilot and technician-related posts.",
        "Class 10 with ITI/diploma/engineering qualification as specified for the post.",
        [
            "Mathematics",
            "Reasoning",
            "General science",
            "Basic science and engineering",
            "Trade knowledge",
        ],
        "Computer-based stages plus computer-based aptitude test for ALP.",
        "Railway Recruitment Boards",
        "https://www.rrbcdg.gov.in",
        "Assistant Loco Pilot and related railway technical posts.",
        [
            "CBT 1",
            "CBT 2",
            "Aptitude test for ALP",
            "Document verification",
            "Medical exam",
        ],
        "As notified by RRB",
        "As notified by RRB",
        "Varies by stage",
        "Computer-based test",
    ),
    exam_record(
        "SBI PO",
        "Banking",
        "Probationary Officer recruitment exam for State Bank of India.",
        "Graduation from a recognized university with age rules as notified.",
        [
            "Reasoning",
            "Data interpretation",
            "English",
            "General/economy/banking awareness",
        ],
        "Prelims, Mains, psychometric test/group exercise/interview as notified.",
        "State Bank of India",
        "https://sbi.co.in/web/careers",
        "Probationary Officer recruitment in SBI.",
        ["Preliminary exam", "Main exam", "Interview/group exercise", "Final merit"],
        "September / October",
        "As notified by SBI",
        "Varies by stage",
        "Computer-based test",
    ),
    exam_record(
        "SBI Clerk",
        "Banking",
        "Junior Associate recruitment exam for State Bank of India.",
        "Graduation from a recognized university with age rules as notified.",
        ["Reasoning", "Numerical ability", "English", "General/financial awareness"],
        "Preliminary and main computer-based exams with language proficiency rules.",
        "State Bank of India",
        "https://sbi.co.in/web/careers",
        "Junior Associate/customer support recruitment in SBI.",
        [
            "Preliminary exam",
            "Main exam",
            "Language proficiency test if applicable",
            "Final merit",
        ],
        "As notified by SBI",
        "As notified by SBI",
        "Varies by stage",
        "Computer-based test",
    ),
    exam_record(
        "IBPS Clerk",
        "Banking",
        "Clerical cadre recruitment exam for participating public sector banks.",
        "Graduation from a recognized university.",
        [
            "Reasoning",
            "Numerical ability",
            "English",
            "General/financial awareness",
            "Computer aptitude",
        ],
        "Preliminary and main computer-based examinations.",
        "Institute of Banking Personnel Selection",
        "https://www.ibps.in",
        "Clerk recruitment in participating public sector banks.",
        ["Preliminary exam", "Main exam", "Provisional allotment"],
        "July / August",
        "August / October",
        "Varies by stage",
        "Computer-based test",
    ),
    exam_record(
        "IBPS RRB",
        "Banking",
        "Recruitment exam for Office Assistant and Officer Scale posts in Regional Rural Banks.",
        "Graduation; post-specific experience and qualifications for some officer scales.",
        [
            "Reasoning",
            "Quantitative aptitude",
            "Computer knowledge",
            "General awareness",
            "Language",
        ],
        "Prelims, Mains/single exam, and interview for officer posts as applicable.",
        "Institute of Banking Personnel Selection",
        "https://www.ibps.in",
        "Recruitment in Regional Rural Banks.",
        [
            "Prelims where applicable",
            "Mains/single exam",
            "Interview for officers",
            "Allotment",
        ],
        "June",
        "August / September",
        "Varies by post",
        "Computer-based test",
    ),
    exam_record(
        "RBI Grade B",
        "Banking",
        "Officer recruitment exam for Grade B posts in Reserve Bank of India.",
        "Graduation/postgraduation requirements vary by stream and notification.",
        [
            "General awareness",
            "Quantitative aptitude",
            "Reasoning",
            "English",
            "Economic and social issues",
            "Finance and management",
        ],
        "Phase I, Phase II, and interview.",
        "Reserve Bank of India",
        "https://opportunities.rbi.org.in",
        "Officer Grade B recruitment in RBI.",
        ["Phase I", "Phase II", "Interview", "Final merit"],
        "As notified by RBI",
        "As notified by RBI",
        "Varies by phase",
        "Computer-based test",
    ),
    exam_record(
        "RBI Assistant",
        "Banking",
        "Assistant recruitment exam for Reserve Bank of India offices.",
        "Graduation with marks/language requirements as per notification.",
        [
            "Reasoning",
            "Numerical ability",
            "English",
            "General awareness",
            "Computer knowledge",
        ],
        "Prelims, Mains, and language proficiency test.",
        "Reserve Bank of India",
        "https://opportunities.rbi.org.in",
        "Assistant posts in RBI.",
        [
            "Preliminary exam",
            "Main exam",
            "Language proficiency test",
            "Final selection",
        ],
        "As notified by RBI",
        "As notified by RBI",
        "Varies by stage",
        "Computer-based test",
    ),
    exam_record(
        "NEET PG",
        "Medical",
        "Postgraduate medical entrance exam for MD/MS/DNB admissions.",
        "MBBS degree, internship completion, and registration as per NMC/NBEMS rules.",
        ["Pre-clinical subjects", "Para-clinical subjects", "Clinical subjects"],
        "Computer-based objective exam.",
        "National Board of Examinations in Medical Sciences",
        "https://natboard.edu.in",
        "Admission to postgraduate medical seats.",
        [
            "Apply online",
            "Appear for NEET PG",
            "Check rank",
            "Participate in counselling",
        ],
        "As notified by NBEMS",
        "As notified by NBEMS",
        "Check latest notification",
        "Computer-based test",
    ),
    exam_record(
        "FMGE",
        "Medical",
        "Screening test for foreign medical graduates seeking registration in India.",
        "Foreign medical degree and eligibility documents as per NMC/NBEMS rules.",
        ["Pre-clinical", "Para-clinical", "Clinical medical subjects"],
        "Computer-based objective screening test.",
        "National Board of Examinations in Medical Sciences",
        "https://natboard.edu.in",
        "Eligibility for medical registration process in India.",
        ["Apply online", "Document verification", "Appear for FMGE", "Download result"],
        "Varies",
        "June / December",
        "Two parts in one day",
        "Computer-based test",
        "Usually twice a year",
    ),
    exam_record(
        "AIIMS NORCET",
        "Medical",
        "Nursing Officer Recruitment Common Eligibility Test.",
        "Nursing qualification and registration as per AIIMS notification.",
        ["Nursing subjects", "General knowledge", "Aptitude"],
        "Computer-based recruitment exam with stages as notified.",
        "All India Institute of Medical Sciences",
        "https://www.aiimsexams.ac.in",
        "Nursing Officer recruitment in AIIMS and participating institutions.",
        ["Apply online", "Computer-based exam", "Result and allocation process"],
        "Varies",
        "Varies",
        "Check latest notification",
        "Computer-based test",
    ),
    exam_record(
        "GPAT",
        "Medical",
        "Graduate Pharmacy Aptitude Test for M.Pharm admission and scholarship use.",
        "Bachelor degree in Pharmacy or final-year eligibility as per notification.",
        [
            "Pharmaceutics",
            "Pharmaceutical chemistry",
            "Pharmacology",
            "Pharmacognosy",
            "Pharmaceutical analysis",
        ],
        "Computer-based objective exam.",
        "National Board of Examinations in Medical Sciences",
        "https://natboard.edu.in",
        "M.Pharm admission and GPAT score-based opportunities.",
        ["Apply online", "Appear for GPAT", "Use score for admission processes"],
        "As notified",
        "As notified",
        "3 hours",
        "Computer-based test",
    ),
    exam_record(
        "Xavier Aptitude Test (XAT)",
        "Management",
        "MBA entrance exam accepted by XLRI and many other management institutes.",
        "Bachelor degree or final-year eligibility as per institute rules.",
        [
            "Verbal ability",
            "Decision making",
            "Quantitative aptitude",
            "Data interpretation",
            "General knowledge",
        ],
        "Computer-based test with institute-specific admission rounds after score release.",
        "XLRI Jamshedpur",
        "https://xatonline.in",
        "MBA/PGDM admission in XAT-accepting institutes.",
        [
            "Register for XAT",
            "Appear for exam",
            "Institute shortlisting",
            "Interview/admission rounds",
        ],
        "July / August",
        "January",
        "About 3 hours",
        "Computer-based test",
    ),
    exam_record(
        "CMAT",
        "Management",
        "Common Management Admission Test for MBA/PGDM admission.",
        "Bachelor degree or final-year eligibility as per notification.",
        [
            "Quantitative techniques",
            "Logical reasoning",
            "Language comprehension",
            "General awareness",
            "Innovation and entrepreneurship",
        ],
        "Computer-based objective test.",
        "National Testing Agency (NTA)",
        "https://exams.nta.ac.in/CMAT/",
        "Admission to management programs in CMAT-accepting institutes.",
        [
            "Apply online",
            "Appear for CMAT",
            "Use score for institute admission process",
        ],
        "March / April",
        "May",
        "3 hours",
        "Computer-based test",
    ),
    exam_record(
        "SNAP",
        "Management",
        "MBA entrance exam for Symbiosis institutes.",
        "Bachelor degree with institute-specific eligibility rules.",
        [
            "General English",
            "Analytical and logical reasoning",
            "Quantitative and data interpretation",
        ],
        "Computer-based objective test.",
        "Symbiosis International University",
        "https://www.snaptest.org",
        "MBA admission in Symbiosis institutes.",
        [
            "Register for SNAP",
            "Appear for test",
            "Apply to institutes",
            "GE-PI-WAT/admission rounds",
        ],
        "August",
        "December",
        "1 hour",
        "Computer-based test",
    ),
    exam_record(
        "NMAT",
        "Management",
        "Management entrance test accepted by NMIMS and other institutes.",
        "Bachelor degree with institute-specific eligibility rules.",
        ["Language skills", "Quantitative skills", "Logical reasoning"],
        "Computer-based test with flexible scheduling window.",
        "Graduate Management Admission Council (GMAC)",
        "https://www.mba.com/exams/nmat",
        "MBA admission in NMAT-accepting institutes.",
        ["Register", "Schedule exam", "Appear for NMAT", "Send scores to schools"],
        "August",
        "October - December",
        "About 2 hours",
        "Computer-based test",
    ),
    exam_record(
        "Graduate Management Admission Test (GMAT)",
        "Management",
        "Global business school admission test for MBA and other graduate management programs.",
        "No fixed academic eligibility for taking the exam; program eligibility depends on each business school.",
        ["Quantitative Reasoning", "Verbal Reasoning", "Data Insights"],
        "Computer-adaptive objective exam with three timed sections.",
        "Graduate Management Admission Council (GMAC)",
        "https://www.mba.com/exams/gmat-exam",
        "Admission to GMAT-accepting MBA, MiM, finance, accounting, and other management programs.",
        [
            "Create an mba.com account",
            "Schedule the test center or online exam",
            "Appear for GMAT",
            "Send scores to selected business schools",
        ],
        "Year-round registration",
        "Available by appointment",
        "About 2 hours 15 minutes",
        "Computer-based adaptive test",
        "Available throughout the year",
        books=[
            "Official GMAT study material from mba.com",
            "GMAT Official Guide",
            "Quantitative Reasoning practice sets",
            "Verbal Reasoning and Data Insights mock tests",
        ],
        tips=[
            "Review the official exam structure before making a study plan",
            "Practice timed Quantitative, Verbal, and Data Insights sections",
            "Analyze mock test score reports for weak areas",
            "Shortlist target schools before sending scores",
        ],
    ),
    exam_record(
        "Common Law Admission Test (CLAT PG)",
        "Law",
        "Entrance exam for postgraduate law programs and some legal recruitment use.",
        "LLB degree or final-year eligibility as per Consortium rules.",
        [
            "Constitutional law",
            "Jurisprudence",
            "Criminal law",
            "Contract law",
            "Torts",
            "Current legal developments",
        ],
        "Offline objective test based on legal passages and core law subjects.",
        "Consortium of National Law Universities",
        "https://consortiumofnlus.ac.in",
        "LLM admission to National Law Universities and score-based opportunities.",
        [
            "Apply online",
            "Appear for CLAT PG",
            "Check rank",
            "Participate in counselling",
        ],
        "July",
        "December",
        "2 hours",
        "Offline pen-and-paper test",
    ),
    exam_record(
        "AILET",
        "Law",
        "Entrance exam for National Law University Delhi programs.",
        "10+2 for BA LLB; LLB for LLM; program-specific rules apply.",
        [
            "English",
            "Current affairs",
            "Logical reasoning",
            "Legal reasoning for PG/advanced law topics where applicable",
        ],
        "Offline objective exam with program-specific pattern.",
        "National Law University Delhi",
        "https://nationallawuniversitydelhi.in",
        "Admission to NLU Delhi law programs.",
        [
            "Apply online",
            "Appear for AILET",
            "Check merit",
            "Complete counselling/admission",
        ],
        "August",
        "December",
        "Varies by program",
        "Offline pen-and-paper test",
    ),
    exam_record(
        "NIFT Entrance Exam",
        "Design",
        "Entrance exam for fashion design, technology, and management programs.",
        "10+2 or degree eligibility depending on selected program.",
        [
            "General ability",
            "Creative ability",
            "Situation test / studio test where applicable",
        ],
        "Written tests and practical/interview stages depending on program.",
        "National Testing Agency (NTA) / NIFT as notified",
        "https://www.nift.ac.in",
        "Admission to NIFT campuses.",
        [
            "Apply online",
            "Appear for written tests",
            "Attend situation test/interview where applicable",
            "Counselling",
        ],
        "December",
        "February",
        "Varies by test",
        "Offline/online as notified",
    ),
    exam_record(
        "NID Design Aptitude Test (NID DAT)",
        "Design",
        "Entrance exam for design programs at National Institute of Design campuses.",
        "10+2 for B.Des; bachelor degree for M.Des as per program rules.",
        ["Design aptitude", "Observation", "Creativity", "Drawing", "Visual reasoning"],
        "DAT Prelims followed by DAT Mains/studio test and interview as applicable.",
        "National Institute of Design",
        "https://www.nid.edu",
        "Admission to NID design programs.",
        ["Apply online", "DAT Prelims", "DAT Mains", "Final merit"],
        "September / October",
        "December / January",
        "Varies by stage",
        "Offline/online as notified",
    ),
    exam_record(
        "UCEED",
        "Design",
        "Undergraduate Common Entrance Examination for Design.",
        "10+2 passed or appearing with age/attempt rules as notified.",
        [
            "Visualization",
            "Observation",
            "Design sensitivity",
            "Analytical reasoning",
            "Drawing",
        ],
        "Computer-based Part A and drawing-based Part B.",
        "IIT Bombay",
        "https://www.uceed.iitb.ac.in",
        "B.Des admission at IITs and participating institutes.",
        [
            "Apply online",
            "Appear for UCEED",
            "Check rank",
            "Apply for B.Des counselling",
        ],
        "October",
        "January",
        "3 hours",
        "Computer-based plus drawing test",
    ),
    exam_record(
        "NATA",
        "Architecture",
        "National Aptitude Test in Architecture for B.Arch admission.",
        "10+2 with mathematics/architecture eligibility as per Council of Architecture rules.",
        [
            "Drawing and composition",
            "Visual reasoning",
            "Mathematics",
            "Architecture aptitude",
        ],
        "Aptitude test assessing architecture readiness and visual ability.",
        "Council of Architecture",
        "https://www.nata.in",
        "B.Arch admission in participating institutions.",
        ["Register for test", "Appear for NATA", "Use score for college admission"],
        "February / March",
        "Multiple windows as notified",
        "3 hours",
        "Computer-based/drawing as notified",
    ),
    exam_record(
        "CA Foundation",
        "Commerce",
        "Entry-level Chartered Accountancy examination.",
        "Class 12 or equivalent route as per ICAI rules.",
        ["Accounting", "Business laws", "Quantitative aptitude", "Business economics"],
        "Combination of objective and descriptive papers.",
        "Institute of Chartered Accountants of India",
        "https://www.icai.org",
        "Entry into the Chartered Accountancy course pathway.",
        [
            "Register with ICAI",
            "Complete study period",
            "Apply for exam",
            "Pass papers to move to Intermediate",
        ],
        "As per ICAI calendar",
        "Multiple attempts as notified",
        "Multiple papers",
        "Offline/online as notified",
        "Multiple times a year",
    ),
    exam_record(
        "CMA Foundation",
        "Commerce",
        "Entry-level Cost and Management Accountancy examination.",
        "Class 12 or equivalent eligibility as per ICMAI rules.",
        [
            "Fundamentals of economics",
            "Accounting",
            "Laws and ethics",
            "Business mathematics and statistics",
        ],
        "Foundation-level papers as notified by ICMAI.",
        "Institute of Cost Accountants of India",
        "https://icmai.in",
        "Entry into the CMA professional course pathway.",
        [
            "Register with ICMAI",
            "Complete required study period",
            "Apply for exam",
            "Pass to move to Intermediate",
        ],
        "As per ICMAI calendar",
        "June / December",
        "Multiple papers",
        "Offline/online as notified",
        "Twice a year",
    ),
    exam_record(
        "CS Executive Entrance Test (CSEET)",
        "Commerce",
        "Entrance test for Company Secretary Executive Programme.",
        "Class 12 or equivalent eligibility as per ICSI rules.",
        [
            "Business communication",
            "Legal aptitude",
            "Economic and business environment",
            "Current affairs",
        ],
        "Remote/online objective test as notified.",
        "Institute of Company Secretaries of India",
        "https://www.icsi.edu",
        "Entry route to CS Executive Programme.",
        [
            "Register with ICSI",
            "Appear for CSEET",
            "Move to Executive Programme after qualifying",
        ],
        "Multiple windows",
        "Multiple windows",
        "2 hours",
        "Online as notified",
        "Multiple times a year",
    ),
]


CATEGORY_ACCENTS = {
    "Engineering": "#2563eb",
    "Medical": "#dc2626",
    "Management": "#7c3aed",
    "Government": "#0f766e",
    "Banking": "#ca8a04",
    "Law": "#9333ea",
    "University": "#0891b2",
    "Teaching": "#16a34a",
    "Defence": "#475569",
    "Railway": "#ea580c",
    "Design": "#db2777",
    "Architecture": "#64748b",
    "Commerce": "#0d9488",
}


EXAM_LOGO_ALIASES = {
    "jee main": "JEE",
    "jee advanced": "IIT",
    "neet ug": "NEET",
    "gate": "GATE",
    "cat": "CAT",
    "upsc cse": "UPSC",
    "ssc cgl": "SSC",
    "ibps po": "IBPS",
    "clat": "CLAT",
    "cuet ug": "CUET",
    "cuet pg": "CUET",
    "ugc net": "NET",
    "ctet": "CTET",
    "nda": "NDA",
    "cds": "CDS",
    "afcat": "AFCAT",
    "ese": "ESE",
    "capf": "CAPF",
    "chsl": "CHSL",
    "mts": "MTS",
    "cpo": "CPO",
    "rrb ntpc": "RRB",
    "rrb group d": "RRB",
    "rrb alp": "ALP",
    "sbi po": "SBI",
    "sbi clerk": "SBI",
    "ibps clerk": "IBPS",
    "ibps rrb": "RRB",
    "rbi grade b": "RBI",
    "rbi assistant": "RBI",
    "neet pg": "NEET",
    "fmge": "FMGE",
    "aiims norcet": "AIIMS",
    "gpat": "GPAT",
    "xat": "XAT",
    "cmat": "CMAT",
    "snap": "SNAP",
    "nmat": "NMAT",
    "gmat": "GMAT",
    "gre": "GRE",
    "ielts": "IELTS",
    "toefl": "TOEFL",
    "sat": "SAT",
    "act": "ACT",
    "lsat": "LSAT",
    "ailet": "AILET",
    "nift": "NIFT",
    "nid dat": "NID",
    "uceed": "UCEED",
    "nata": "NATA",
    "ca foundation": "ICAI",
    "cma foundation": "ICMAI",
    "cseet": "ICSI",
}


def make_exam_logo_text(exam):
    name = exam["name"].lower()
    compact_name = " ".join("".join(ch.lower() if ch.isalnum() else " " for ch in exam["name"]).split())
    for key, logo in EXAM_LOGO_ALIASES.items():
        if key in name or key in compact_name:
            return logo

    uppercase_tokens = [
        "".join(ch for ch in token if ch.isalpha())
        for token in exam["name"].replace("(", " ").replace(")", " ").split()
        if token.isupper()
    ]
    acronym = "".join(token[0] for token in uppercase_tokens if token)
    if len(acronym) >= 2:
        return acronym[:5]

    words = [
        "".join(ch for ch in token if ch.isalnum())
        for token in exam["name"].replace("(", " ").replace(")", " ").split()
    ]
    initials = "".join(word[0].upper() for word in words if word and word[0].isalpha())
    return initials[:4] or "EXAM"


LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn",
    "Tamil": "ta",
    "Telugu": "te",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Urdu": "ur",
    "Spanish": "es",
    "French": "fr",
}


UI_TEXT = {
    "en": {
        "app_tagline": "Find the right exam path faster.",
        "language": "Language",
        "search_exams": "Search exams",
        "category": "Category",
        "total_exams": "Total exams",
        "categories": "Categories",
        "hero_kicker": "Plan. Compare. Prepare.",
        "hero_label": "Exam intelligence workspace",
        "hero_copy": (
            "Discover, compare, and prepare for competitive exams with structured facts, "
            "trusted official links, and preparation paths in one focused workspace."
        ),
        "curated_exams": "Curated exams",
        "exam_categories": "Exam categories",
        "current_matches": "Current matches",
        "computer_based": "Computer-based exams",
        "management_exams": "Management exams",
        "official_links": "Official links included",
        "paper_search": "Previous year paper search",
        "matching_exams": "Matching exams",
        "view_details": "View exam details",
        "results": "result",
        "no_results": "No exams found. Try a different search term or category.",
        "select_prompt": (
            "Click View exam details on any matching exam to view eligibility, dates, syllabus, and prep guidance."
        ),
        "exam_details": "Exam details",
        "close_details": "Close details",
        "overview": "Overview",
        "syllabus": "Syllabus",
        "preparation": "Preparation",
        "apply": "Apply",
        "eligibility": "Eligibility",
        "exam_pattern": "Exam pattern",
        "conducted_by": "Conducted by",
        "frequency": "Frequency",
        "exam_mode": "Exam mode",
        "duration": "Duration",
        "application_mode": "Application mode",
        "fee": "Fee",
        "used_for": "Used for",
        "important_dates": "Important dates",
        "stage": "Stage",
        "notification": "Notification",
        "exam_date": "Exam date",
        "timeline": "Timeline",
        "syllabus_focus": "Syllabus focus",
        "selection_process": "Selection process",
        "recommended_books": "Recommended books and study material",
        "book_note": "Compare edition, seller rating, and latest price before buying.",
        "buy_amazon": "Buy on Amazon",
        "buy_flipkart": "Buy on Flipkart",
        "preparation_tips": "Preparation tips",
        "pyq": "Previous year question papers",
        "official_website": "Open official website",
        "how_apply": "How to apply",
        "check_notice": "Check notice",
        "check_latest": "Check latest notification",
        "to_be_announced": "To be announced",
    },
    "hi": {
        "app_tagline": "सही परीक्षा मार्ग तेजी से खोजें।",
        "language": "भाषा",
        "search_exams": "परीक्षा खोजें",
        "category": "श्रेणी",
        "total_exams": "कुल परीक्षाएं",
        "categories": "श्रेणियां",
        "hero_kicker": "योजना बनाएं। तुलना करें। तैयारी करें।",
        "hero_label": "परीक्षा जानकारी कार्यक्षेत्र",
        "hero_copy": "संरचित जानकारी, आधिकारिक लिंक और तैयारी मार्ग के साथ प्रतियोगी परीक्षाओं को खोजें, तुलना करें और तैयारी करें।",
        "matching_exams": "मिलती हुई परीक्षाएं",
        "view_details": "परीक्षा विवरण देखें",
        "exam_details": "परीक्षा विवरण",
        "close_details": "विवरण बंद करें",
        "overview": "सारांश",
        "syllabus": "पाठ्यक्रम",
        "preparation": "तैयारी",
        "apply": "आवेदन",
        "eligibility": "योग्यता",
        "exam_pattern": "परीक्षा पैटर्न",
        "important_dates": "महत्वपूर्ण तिथियां",
        "recommended_books": "अनुशंसित पुस्तकें और अध्ययन सामग्री",
        "buy_amazon": "Amazon पर खरीदें",
        "buy_flipkart": "Flipkart पर खरीदें",
    },
    "kn": {
        "app_tagline": "ಸರಿಯಾದ ಪರೀಕ್ಷಾ ಮಾರ್ಗವನ್ನು ಬೇಗ ಕಂಡುಕೊಳ್ಳಿ.",
        "language": "ಭಾಷೆ",
        "search_exams": "ಪರೀಕ್ಷೆಗಳನ್ನು ಹುಡುಕಿ",
        "category": "ವರ್ಗ",
        "matching_exams": "ಹೊಂದುವ ಪರೀಕ್ಷೆಗಳು",
        "view_details": "ಪರೀಕ್ಷೆಯ ವಿವರ ನೋಡಿ",
        "exam_details": "ಪರೀಕ್ಷೆಯ ವಿವರಗಳು",
        "overview": "ಸಾರಾಂಶ",
        "syllabus": "ಪಠ್ಯಕ್ರಮ",
        "preparation": "ತಯಾರಿ",
        "apply": "ಅರ್ಜಿ",
    },
    "ta": {
        "app_tagline": "சரியான தேர்வு பாதையை விரைவாக கண்டறியுங்கள்.",
        "language": "மொழி",
        "search_exams": "தேர்வுகளை தேடுங்கள்",
        "category": "வகை",
        "matching_exams": "பொருந்தும் தேர்வுகள்",
        "view_details": "தேர்வு விவரங்களை காண்க",
        "exam_details": "தேர்வு விவரங்கள்",
        "overview": "கண்ணோட்டம்",
        "syllabus": "பாடத்திட்டம்",
        "preparation": "தயாரிப்பு",
        "apply": "விண்ணப்பம்",
    },
    "te": {
        "app_tagline": "సరైన పరీక్ష మార్గాన్ని త్వరగా కనుగొనండి.",
        "language": "భాష",
        "search_exams": "పరీక్షలను వెతకండి",
        "category": "వర్గం",
        "matching_exams": "సరిపోయే పరీక్షలు",
        "view_details": "పరీక్ష వివరాలు చూడండి",
        "exam_details": "పరీక్ష వివరాలు",
        "overview": "అవలోకనం",
        "syllabus": "సిలబస్",
        "preparation": "తయారీ",
        "apply": "దరఖాస్తు",
    },
    "ml": {
        "app_tagline": "ശരിയായ പരീക്ഷാ വഴി വേഗത്തിൽ കണ്ടെത്തുക.",
        "language": "ഭാഷ",
        "search_exams": "പരീക്ഷകൾ തിരയുക",
        "category": "വിഭാഗം",
        "matching_exams": "പൊരുത്തപ്പെടുന്ന പരീക്ഷകൾ",
        "view_details": "പരീക്ഷാ വിവരങ്ങൾ കാണുക",
        "exam_details": "പരീക്ഷാ വിവരങ്ങൾ",
        "overview": "അവലോകനം",
        "syllabus": "സിലബസ്",
        "preparation": "തയ്യാറെടുപ്പ്",
        "apply": "അപേക്ഷ",
    },
    "mr": {
        "app_tagline": "योग्य परीक्षा मार्ग लवकर शोधा.",
        "language": "भाषा",
        "search_exams": "परीक्षा शोधा",
        "category": "वर्ग",
        "matching_exams": "जुळणाऱ्या परीक्षा",
        "view_details": "परीक्षेचे तपशील पहा",
        "exam_details": "परीक्षेचे तपशील",
        "overview": "आढावा",
        "syllabus": "अभ्यासक्रम",
        "preparation": "तयारी",
        "apply": "अर्ज",
    },
    "bn": {
        "app_tagline": "সঠিক পরীক্ষার পথ দ্রুত খুঁজুন।",
        "language": "ভাষা",
        "search_exams": "পরীক্ষা খুঁজুন",
        "category": "বিভাগ",
        "matching_exams": "মিল থাকা পরীক্ষা",
        "view_details": "পরীক্ষার বিবরণ দেখুন",
        "exam_details": "পরীক্ষার বিবরণ",
        "overview": "সারাংশ",
        "syllabus": "সিলেবাস",
        "preparation": "প্রস্তুতি",
        "apply": "আবেদন",
    },
    "gu": {
        "app_tagline": "યોગ્ય પરીક્ષા માર્ગ ઝડપથી શોધો.",
        "language": "ભાષા",
        "search_exams": "પરીક્ષા શોધો",
        "category": "વર્ગ",
        "matching_exams": "મેળ ખાતી પરીક્ષાઓ",
        "view_details": "પરીક્ષાની વિગતો જુઓ",
        "exam_details": "પરીક્ષાની વિગતો",
        "overview": "સારાંશ",
        "syllabus": "અભ્યાસક્રમ",
        "preparation": "તૈયારી",
        "apply": "અરજી",
    },
    "pa": {
        "app_tagline": "ਸਹੀ ਪ੍ਰੀਖਿਆ ਰਾਹ ਜਲਦੀ ਲੱਭੋ।",
        "language": "ਭਾਸ਼ਾ",
        "search_exams": "ਪ੍ਰੀਖਿਆਵਾਂ ਖੋਜੋ",
        "category": "ਸ਼੍ਰੇਣੀ",
        "matching_exams": "ਮਿਲਦੀਆਂ ਪ੍ਰੀਖਿਆਵਾਂ",
        "view_details": "ਪ੍ਰੀਖਿਆ ਵੇਰਵੇ ਵੇਖੋ",
        "exam_details": "ਪ੍ਰੀਖਿਆ ਵੇਰਵੇ",
        "overview": "ਝਲਕ",
        "syllabus": "ਸਿਲੇਬਸ",
        "preparation": "ਤਿਆਰੀ",
        "apply": "ਅਰਜ਼ੀ",
    },
    "ur": {
        "app_tagline": "صحیح امتحان کا راستہ تیزی سے تلاش کریں۔",
        "language": "زبان",
        "search_exams": "امتحانات تلاش کریں",
        "category": "زمرہ",
        "matching_exams": "ملتے جلتے امتحانات",
        "view_details": "امتحان کی تفصیل دیکھیں",
        "exam_details": "امتحان کی تفصیلات",
        "overview": "جائزہ",
        "syllabus": "نصاب",
        "preparation": "تیاری",
        "apply": "درخواست",
    },
    "es": {
        "app_tagline": "Encuentra más rápido tu camino de examen.",
        "language": "Idioma",
        "search_exams": "Buscar exámenes",
        "category": "Categoría",
        "matching_exams": "Exámenes coincidentes",
        "view_details": "Ver detalles del examen",
        "exam_details": "Detalles del examen",
        "overview": "Resumen",
        "syllabus": "Temario",
        "preparation": "Preparación",
        "apply": "Aplicar",
    },
    "fr": {
        "app_tagline": "Trouvez plus vite le bon parcours d'examen.",
        "language": "Langue",
        "search_exams": "Rechercher des examens",
        "category": "Catégorie",
        "matching_exams": "Examens correspondants",
        "view_details": "Voir les détails",
        "exam_details": "Détails de l'examen",
        "overview": "Aperçu",
        "syllabus": "Programme",
        "preparation": "Préparation",
        "apply": "Postuler",
    },
}


def tr(key, language_code="en"):
    return UI_TEXT.get(language_code, {}).get(key, UI_TEXT["en"][key])


@st.cache_data(show_spinner=False)
def translate_text(text, language_code="en"):
    if language_code == "en" or not text:
        return text
    query = urlencode(
        {
            "client": "gtx",
            "sl": "auto",
            "tl": language_code,
            "dt": "t",
            "q": text,
        }
    )
    url = f"https://translate.googleapis.com/translate_a/single?{query}"
    try:
        with urlopen(url, timeout=4) as response:  # nosec B310 - fixed HTTPS translation endpoint.
            payload = loads(response.read().decode("utf-8"))
        translated = "".join(part[0] for part in payload[0] if part and part[0])
        return translated or text
    except (HTTPError, URLError, TimeoutError, JSONDecodeError, UnicodeDecodeError, IndexError, TypeError):
        return text


def inject_theme():  # pragma: no cover
    st.markdown(
        """
        <style>
        :root {
            --ink: var(--text-color);
            --muted: color-mix(in srgb, var(--text-color) 60%, transparent);
            --line: color-mix(in srgb, var(--text-color) 16%, transparent);
            --panel: var(--secondary-background-color);
            --panel-2: var(--background-color);
            --canvas: var(--background-color);
            --brand: var(--primary-color);
            --brand-2: #00a7a5;
            --soft-panel: color-mix(in srgb, var(--secondary-background-color) 88%, var(--background-color) 12%);
            --chip: color-mix(in srgb, var(--text-color) 8%, var(--background-color) 92%);
            --shadow: color-mix(in srgb, #000000 18%, transparent);
        }

        .stApp {
            background:
                radial-gradient(circle at top left, color-mix(in srgb, var(--brand) 14%, transparent), transparent 34%),
                radial-gradient(
                    circle at top right,
                    color-mix(in srgb, var(--brand-2) 10%, transparent),
                    transparent 30%
                ),
                var(--background-color);
            color: var(--ink);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1180px;
        }

        section[data-testid="stSidebar"] {
            background: var(--secondary-background-color);
            border-right: 1px solid var(--line);
        }

        section[data-testid="stSidebar"] * {
            color: var(--ink);
        }

        section[data-testid="stSidebar"] input {
            background: var(--background-color);
            color: var(--text-color);
        }

        section[data-testid="stSidebar"] input::placeholder {
            color: var(--muted);
        }

        section[data-testid="stSidebar"] [data-baseweb="select"] > div {
            background: var(--background-color);
            border-color: var(--line);
        }

        section[data-testid="stSidebar"] [data-baseweb="select"] span,
        section[data-testid="stSidebar"] [data-baseweb="select"] svg {
            color: var(--text-color);
            fill: var(--text-color);
        }

        .stTabs [data-baseweb="tab-list"] {
            border-bottom: 1px solid var(--line);
        }

        .stTabs [data-baseweb="tab"] {
            color: var(--muted);
        }

        .stTabs [aria-selected="true"] {
            color: var(--brand);
        }

        .stButton button,
        div[data-testid="stButton"] button {
            border: 1px solid #2152ff !important;
            background: linear-gradient(135deg, #2152ff, #00a7a5) !important;
            color: #ffffff !important;
            font-weight: 850 !important;
            min-height: 44px !important;
            border-radius: 10px !important;
            box-shadow: 0 10px 24px rgba(33, 82, 255, 0.24) !important;
            opacity: 1 !important;
            transition:
                transform 180ms ease,
                box-shadow 180ms ease,
                filter 180ms ease !important;
        }

        .stButton button p,
        .stButton button span,
        div[data-testid="stButton"] button p,
        div[data-testid="stButton"] button span {
            color: #ffffff !important;
            font-weight: 850 !important;
            opacity: 1 !important;
        }

        .stButton button:hover,
        div[data-testid="stButton"] button:hover {
            border-color: #173ed6 !important;
            filter: brightness(1.04);
            transform: translateY(-1px);
            box-shadow: 0 14px 30px rgba(33, 82, 255, 0.3) !important;
        }

        div[data-testid="stDataFrame"],
        div[data-testid="stTable"] {
            color: var(--ink);
        }

        .eh-hero {
            border: 1px solid rgba(23, 32, 51, 0.08);
            border-radius: 18px;
            padding: 30px;
            background:
                linear-gradient(135deg, rgba(16, 24, 40, 0.98), rgba(37, 70, 202, 0.92)),
                linear-gradient(45deg, rgba(45, 212, 191, 0.26), transparent);
            background-size: 180% 180%;
            color: #ffffff;
            box-shadow: 0 22px 54px var(--shadow);
            margin-bottom: 22px;
            position: relative;
            overflow: hidden;
            isolation: isolate;
            animation:
                eh-fade-up 620ms ease-out both,
                eh-hero-gradient 9s ease-in-out infinite;
            transition:
                transform 220ms ease,
                box-shadow 220ms ease,
                border-color 220ms ease;
        }

        .eh-hero:hover {
            transform: translateY(-4px);
            border-color: rgba(45, 212, 191, 0.54);
            box-shadow:
                0 28px 68px rgba(15, 23, 42, 0.36),
                0 0 0 1px rgba(45, 212, 191, 0.18),
                0 0 42px rgba(45, 212, 191, 0.22);
        }

        .eh-hero::before {
            content: "";
            position: absolute;
            left: 18px;
            right: 18px;
            top: 0;
            height: 4px;
            border-radius: 999px;
            background: linear-gradient(90deg, transparent, #2dd4bf, #ffffff, #8ea4ff, transparent);
            opacity: 0.48;
            transform: translateX(-42%);
            animation: eh-top-pulse 3.2s ease-in-out infinite;
            pointer-events: none;
            z-index: 0;
        }

        .eh-hero::after {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(110deg, transparent 0%, rgba(255, 255, 255, 0.2) 42%, transparent 64%),
                repeating-linear-gradient(
                    90deg,
                    rgba(255, 255, 255, 0.055) 0,
                    rgba(255, 255, 255, 0.055) 1px,
                    transparent 1px,
                    transparent 34px
                );
            opacity: 0.82;
            transform: translateX(-120%);
            animation:
                eh-sheen 5.2s ease-in-out 700ms infinite,
                eh-grid-drift 11s linear infinite;
            pointer-events: none;
            z-index: 0;
        }

        .eh-hero:hover::after {
            opacity: 1;
            animation:
                eh-sheen 2.4s ease-in-out infinite,
                eh-grid-drift 5.5s linear infinite;
        }

        .eh-hero > * {
            position: relative;
            z-index: 1;
        }

        .eh-kicker {
            color: rgba(255, 255, 255, 0.74);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }

        .eh-brand {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 26px;
        }

        .eh-logo {
            width: 54px;
            height: 54px;
            border-radius: 16px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background:
                linear-gradient(135deg, #ffffff 0%, #d7fff7 46%, #b7c8ff 100%);
            color: #172033;
            font-size: 1.15rem;
            font-weight: 900;
            letter-spacing: 0;
            box-shadow: 0 16px 34px rgba(0, 0, 0, 0.22);
            animation:
                eh-float 4.8s ease-in-out infinite,
                eh-logo-glow 2.8s ease-in-out infinite;
            transition:
                transform 220ms ease,
                box-shadow 220ms ease;
        }

        .eh-hero:hover .eh-logo {
            animation: none;
            transform: translateY(-5px) rotate(-3deg) scale(1.06);
            box-shadow:
                0 18px 38px rgba(0, 0, 0, 0.26),
                0 0 34px rgba(45, 212, 191, 0.46);
        }

        .eh-brand-text {
            color: rgba(255, 255, 255, 0.86);
            font-size: 0.86rem;
            font-weight: 800;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .eh-sidebar-brand {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 4px 0 18px;
        }

        .eh-sidebar-logo {
            width: 38px;
            height: 38px;
            border-radius: 12px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #ffffff 0%, #d7fff7 46%, #b7c8ff 100%);
            color: #172033;
            font-size: 0.86rem;
            font-weight: 900;
        }

        .eh-sidebar-name {
            color: var(--ink);
            font-size: 1rem;
            font-weight: 850;
            line-height: 1.1;
        }

        .eh-hero h1 {
            color: #ffffff;
            font-size: 3rem;
            line-height: 1.05;
            margin: 0 0 12px;
            letter-spacing: 0;
        }

        .eh-hero p {
            color: rgba(255, 255, 255, 0.86);
            font-size: 1.02rem;
            max-width: 740px;
            margin: 0;
        }

        .eh-stat-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 12px;
            margin-bottom: 18px;
        }

        .eh-stat {
            border: 1px solid var(--line);
            border-radius: 12px;
            background: var(--soft-panel);
            padding: 16px;
            box-shadow: 0 14px 34px var(--shadow);
            animation: eh-fade-up 520ms ease-out both;
            transition:
                transform 180ms ease,
                box-shadow 180ms ease,
                border-color 180ms ease;
        }

        .eh-stat:hover {
            transform: translateY(-3px);
            box-shadow: 0 18px 40px var(--shadow);
            border-color: color-mix(in srgb, var(--brand) 28%, var(--line));
        }

        .eh-stat-value {
            color: var(--ink);
            font-size: 1.55rem;
            font-weight: 800;
            line-height: 1;
        }

        .eh-stat-label {
            color: var(--muted);
            font-size: 0.78rem;
            margin-top: 7px;
        }

        .eh-card {
            border: 1px solid var(--line);
            border-radius: 14px;
            background: var(--soft-panel);
            padding: 18px;
            margin-bottom: 14px;
            box-shadow: 0 14px 34px var(--shadow);
            animation: eh-fade-up 560ms ease-out both;
            transition:
                transform 180ms ease,
                box-shadow 180ms ease,
                border-color 180ms ease;
        }

        .eh-card:hover {
            transform: translateY(-3px);
            box-shadow:
                0 18px 42px var(--shadow),
                0 0 30px color-mix(in srgb, var(--accent, var(--brand)) 14%, transparent);
            border-color: color-mix(in srgb, var(--accent, var(--brand)) 26%, var(--line));
        }

        .eh-exam-card {
            border-left: 5px solid var(--accent);
        }

        .eh-result-card {
            height: 328px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            overflow: hidden;
        }

        .eh-exam-header {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 10px;
        }

        .eh-exam-logo {
            width: 54px;
            height: 54px;
            flex: 0 0 54px;
            border: 1px solid color-mix(in srgb, var(--accent) 24%, var(--line));
            border-radius: 14px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background:
                linear-gradient(135deg, var(--accent-bg), rgba(255, 255, 255, 0.72)),
                var(--soft-panel);
            color: var(--accent);
            font-size: 0.78rem;
            font-weight: 900;
            line-height: 1;
            text-align: center;
            overflow-wrap: anywhere;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.6);
            animation: eh-logo-pop 520ms cubic-bezier(0.2, 0.9, 0.2, 1.15) both;
            transition:
                transform 180ms ease,
                box-shadow 180ms ease,
                background 180ms ease;
        }

        .eh-card:hover .eh-exam-logo {
            transform: scale(1.06) rotate(-2deg);
            box-shadow:
                inset 0 1px 0 rgba(255, 255, 255, 0.68),
                0 10px 22px color-mix(in srgb, var(--accent) 28%, transparent),
                0 0 18px color-mix(in srgb, var(--accent) 30%, transparent);
        }

        .eh-exam-title-block {
            min-width: 0;
            flex: 1;
        }

        .eh-result-card h3 {
            min-height: 3.55rem;
            max-height: 3.55rem;
            overflow: hidden;
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 2;
        }

        .eh-result-card p {
            min-height: 5.4rem;
            max-height: 5.4rem;
            overflow: hidden;
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 3;
        }

        .eh-result-card .eh-pill-row {
            min-height: 74px;
            align-content: flex-start;
            overflow: hidden;
        }

        .eh-card h3 {
            color: var(--ink);
            font-size: 1.1rem;
            line-height: 1.25;
            margin: 0 0 8px;
            letter-spacing: 0;
        }

        .eh-card p {
            color: var(--muted);
            font-size: 0.92rem;
            margin: 0;
        }

        .eh-passport {
            display: grid;
            grid-template-columns: 1.4fr repeat(2, minmax(0, 0.8fr));
            gap: 14px;
            margin: 14px 0 18px;
        }

        .eh-passport-panel {
            border: 1px solid var(--line);
            border-radius: 14px;
            background:
                linear-gradient(
                    180deg,
                    var(--soft-panel),
                    color-mix(in srgb, var(--panel) 82%, var(--background-color) 18%)
                ),
                linear-gradient(135deg, var(--accent-bg), transparent 48%);
            padding: 16px;
            min-height: 118px;
        }

        .eh-passport-label {
            color: var(--muted);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .eh-passport-value {
            color: var(--ink);
            font-size: 1.08rem;
            font-weight: 850;
            line-height: 1.35;
        }

        .eh-fact-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
            margin: 16px 0 24px;
        }

        .eh-fact {
            border: 1px solid var(--line);
            border-radius: 12px;
            background: var(--soft-panel);
            padding: 13px;
            box-shadow: 0 10px 24px var(--shadow);
        }

        .eh-fact-label {
            color: var(--muted);
            font-size: 0.72rem;
            font-weight: 800;
            margin-bottom: 7px;
        }

        .eh-fact-value {
            color: var(--ink);
            font-size: 0.95rem;
            font-weight: 800;
            line-height: 1.25;
        }

        .eh-info-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 14px;
            margin-top: 14px;
        }

        .eh-info-panel {
            border: 1px solid var(--line);
            border-radius: 14px;
            background: var(--soft-panel);
            padding: 16px;
            min-height: 126px;
            animation: eh-fade-up 520ms ease-out both;
        }

        .eh-info-panel-wide {
            grid-column: 1 / -1;
        }

        .eh-info-title {
            color: var(--ink);
            font-size: 0.92rem;
            font-weight: 850;
            margin-bottom: 10px;
        }

        .eh-info-copy {
            color: var(--muted);
            font-size: 0.95rem;
            line-height: 1.55;
        }

        .eh-book-card {
            border: 1px solid var(--line);
            border-radius: 14px;
            background: var(--soft-panel);
            padding: 14px;
            margin-bottom: 12px;
            transition:
                transform 180ms ease,
                border-color 180ms ease,
                box-shadow 180ms ease;
        }

        .eh-book-card:hover {
            transform: translateX(3px);
            border-color: color-mix(in srgb, var(--brand-2) 30%, var(--line));
            box-shadow: 0 10px 24px var(--shadow);
        }

        .eh-book-title {
            color: var(--ink);
            font-size: 0.95rem;
            font-weight: 850;
            line-height: 1.35;
            margin-bottom: 6px;
        }

        .eh-book-note {
            color: var(--muted);
            font-size: 0.78rem;
            margin-bottom: 10px;
        }

        .eh-chip-list {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 8px;
        }

        .eh-pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 12px 0 0;
        }

        .eh-pill {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            background: var(--chip);
            color: var(--ink);
            font-size: 0.75rem;
            font-weight: 700;
            padding: 6px 10px;
            transition:
                transform 160ms ease,
                background 160ms ease;
        }

        .eh-pill:hover {
            transform: translateY(-1px);
        }

        .eh-category-pill {
            background: var(--accent-bg);
            color: var(--accent);
        }

        .eh-section-title {
            color: var(--ink);
            font-size: 1.05rem;
            font-weight: 800;
            margin: 4px 0 12px;
        }

        .eh-timeline {
            display: grid;
            gap: 10px;
        }

        .eh-step {
            border-left: 3px solid var(--brand-2);
            padding-left: 12px;
            color: var(--muted);
        }

        .eh-insight-grid {
            display: grid;
            grid-template-columns: 0.9fr 1.1fr;
            gap: 14px;
            margin: 8px 0 18px;
        }

        .eh-orbit {
            position: relative;
            min-height: 210px;
            border: 1px solid var(--line);
            border-radius: 16px;
            background:
                radial-gradient(circle at center, color-mix(in srgb, var(--brand) 20%, transparent), transparent 42%),
                var(--soft-panel);
            overflow: hidden;
        }

        .eh-orbit::before,
        .eh-orbit::after {
            content: "";
            position: absolute;
            inset: 34px;
            border: 1px solid color-mix(in srgb, var(--brand) 34%, transparent);
            border-radius: 50%;
            animation: eh-spin 12s linear infinite;
        }

        .eh-orbit::after {
            inset: 58px;
            border-color: color-mix(in srgb, var(--brand-2) 40%, transparent);
            animation-duration: 8s;
            animation-direction: reverse;
        }

        .eh-orbit-core {
            position: absolute;
            inset: 50%;
            width: 86px;
            height: 86px;
            transform: translate(-50%, -50%);
            border-radius: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, var(--brand), var(--brand-2));
            color: #ffffff;
            font-weight: 900;
            font-size: 1.4rem;
            box-shadow: 0 16px 36px var(--shadow);
            z-index: 1;
        }

        .eh-bars {
            border: 1px solid var(--line);
            border-radius: 16px;
            background: var(--soft-panel);
            padding: 16px;
        }

        .eh-bar-row {
            margin-bottom: 14px;
        }

        .eh-bar-label {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            color: var(--ink);
            font-size: 0.82rem;
            font-weight: 800;
            margin-bottom: 7px;
        }

        .eh-bar-track {
            height: 10px;
            border-radius: 999px;
            background: color-mix(in srgb, var(--text-color) 10%, var(--background-color) 90%);
            overflow: hidden;
        }

        .eh-bar-fill {
            height: 100%;
            width: var(--value);
            border-radius: inherit;
            background: linear-gradient(90deg, var(--brand), var(--brand-2));
            animation: eh-grow 900ms ease-out both;
        }

        @keyframes eh-grow {
            from {
                width: 0;
            }
            to {
                width: var(--value);
            }
        }

        @keyframes eh-fade-up {
            from {
                opacity: 0;
                transform: translateY(14px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes eh-logo-pop {
            from {
                opacity: 0;
                transform: scale(0.82);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }

        @keyframes eh-float {
            0%,
            100% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(-5px);
            }
        }

        @keyframes eh-logo-glow {
            0%,
            100% {
                box-shadow: 0 16px 34px rgba(0, 0, 0, 0.22);
            }
            50% {
                box-shadow:
                    0 16px 34px rgba(0, 0, 0, 0.22),
                    0 0 24px rgba(45, 212, 191, 0.4);
            }
        }

        @keyframes eh-hero-gradient {
            0%,
            100% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
        }

        @keyframes eh-top-pulse {
            0%,
            100% {
                opacity: 0.42;
                transform: translateX(-42%);
            }
            50% {
                opacity: 1;
                transform: translateX(42%);
            }
        }

        @keyframes eh-grid-drift {
            from {
                background-position: 0 0, 0 0;
            }
            to {
                background-position: 0 0, 68px 0;
            }
        }

        @keyframes eh-sheen {
            0%,
            38% {
                transform: translateX(-120%);
            }
            62%,
            100% {
                transform: translateX(120%);
            }
        }

        @keyframes eh-spin {
            from {
                transform: rotate(0deg);
            }
            to {
                transform: rotate(360deg);
            }
        }

        @media (max-width: 900px) {
            .eh-stat-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .eh-passport,
            .eh-fact-grid,
            .eh-info-grid,
            .eh-insight-grid {
                grid-template-columns: 1fr;
            }

            .eh-info-panel-wide {
                grid-column: auto;
            }

            .eh-hero h1 {
                font-size: 2.25rem;
            }
        }

        @media (prefers-reduced-motion: reduce) {
            *,
            *::before,
            *::after {
                animation-duration: 1ms !important;
                animation-iteration-count: 1 !important;
                scroll-behavior: auto !important;
                transition-duration: 1ms !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(language_code):  # pragma: no cover
    st.markdown(
        f"""
        <div class="eh-hero">
            <div class="eh-brand">
                <div class="eh-logo">EH</div>
                <div>
                    <div class="eh-brand-text">{escape(tr("hero_label", language_code))}</div>
                    <div class="eh-kicker">{escape(tr("hero_kicker", language_code))}</div>
                </div>
            </div>
            <h1>Exam Hub</h1>
            <p>
                {escape(tr("hero_copy", language_code))}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stat_grid(exams, filtered_exams, categories, language_code):  # pragma: no cover
    management_count = sum(1 for exam in exams if exam["category"] == "Management")
    online_count = sum(1 for exam in exams if "computer" in exam.get("examMode", "").lower())
    st.markdown(
        f"""
        <div class="eh-stat-grid">
            <div class="eh-stat">
                <div class="eh-stat-value">{len(exams)}</div>
                <div class="eh-stat-label">{escape(tr("curated_exams", language_code))}</div>
            </div>
            <div class="eh-stat">
                <div class="eh-stat-value">{len(categories) - 1}</div>
                <div class="eh-stat-label">{escape(tr("exam_categories", language_code))}</div>
            </div>
            <div class="eh-stat">
                <div class="eh-stat-value">{len(filtered_exams)}</div>
                <div class="eh-stat-label">{escape(tr("current_matches", language_code))}</div>
            </div>
            <div class="eh-stat">
                <div class="eh-stat-value">{online_count}</div>
                <div class="eh-stat-label">{escape(tr("computer_based", language_code))}</div>
            </div>
        </div>
        <div class="eh-pill-row">
            <span class="eh-pill">{escape(tr("management_exams", language_code))}: {management_count}</span>
            <span class="eh-pill">{escape(tr("official_links", language_code))}</span>
            <span class="eh-pill">{escape(tr("paper_search", language_code))}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_exam_preview(exam, language_code):  # pragma: no cover
    accent = CATEGORY_ACCENTS.get(exam["category"], "#2152ff")
    category = translate_text(exam["category"], language_code)
    exam_mode = translate_text(exam.get("examMode", tr("check_notice", language_code)), language_code)
    duration = translate_text(exam.get("duration", tr("check_notice", language_code)), language_code)
    logo_text = escape(exam.get("logoText", make_exam_logo_text(exam)))
    st.markdown(
        f"""
        <div class="eh-card eh-exam-card eh-result-card" style="--accent: {accent}; --accent-bg: {accent}18;">
            <div class="eh-exam-header">
                <div class="eh-exam-logo" aria-label="{escape(exam["name"])} logo">{logo_text}</div>
                <div class="eh-exam-title-block">
                    <h3>{escape(translate_text(exam["name"], language_code))}</h3>
                </div>
            </div>
            <p>{escape(translate_text(exam["description"], language_code))}</p>
            <div class="eh-pill-row">
                <span class="eh-pill eh-category-pill">{escape(category)}</span>
                <span class="eh-pill">{escape(exam_mode)}</span>
                <span class="eh-pill">{escape(duration)}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_overview_panel(title, value, wide=False):  # pragma: no cover
    wide_class = " eh-info-panel-wide" if wide else ""
    return (
        f'<div class="eh-info-panel{wide_class}">'
        f'<div class="eh-info-title">{escape(title)}</div>'
        f'<div class="eh-info-copy">{escape(value)}</div>'
        "</div>"
    )


def render_section_title(key, language_code):  # pragma: no cover
    st.markdown(
        f'<div class="eh-section-title">{escape(tr(key, language_code))}</div>',
        unsafe_allow_html=True,
    )


def render_book_card(book, language_code):  # pragma: no cover
    st.markdown(
        f"""
        <div class="eh-book-card">
            <div class="eh-book-title">{escape(translate_text(book, language_code))}</div>
            <div class="eh-book-note">{escape(tr("book_note", language_code))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    links = make_book_links(book)
    amazon_col, flipkart_col = st.columns(2)
    amazon_col.link_button(tr("buy_amazon", language_code), links["Amazon"], use_container_width=True)
    flipkart_col.link_button(tr("buy_flipkart", language_code), links["Flipkart"], use_container_width=True)


@st.dialog("Exam details", width="large")
def render_exam_dialog(exam, language_code):  # pragma: no cover
    render_exam_details(exam, language_code)
    if st.button(tr("close_details", language_code), use_container_width=True):
        st.session_state.selected_exam_id = None
        st.rerun()


@st.cache_data
def load_exams():
    exams = []
    for index, exam in enumerate(BASE_EXAMS + ADDITIONAL_EXAMS, start=1):
        item = deepcopy(exam)
        short_name = item["name"].split("(")[0].strip()
        item["id"] = index
        item["logoText"] = make_exam_logo_text(item)
        item["pyq"] = make_pyqs(short_name)
        item["applicationSteps"] = APPLICATION_STEPS
        exams.append(item)
    return exams


def matches_filters(exam, query, category):
    query_matches = not query or query in exam["name"].lower() or query in exam["description"].lower()
    category_matches = category == "All categories" or exam["category"] == category
    return query_matches and category_matches


def render_exam_details(exam, language_code):  # pragma: no cover
    accent = CATEGORY_ACCENTS.get(exam["category"], "#2152ff")
    category = translate_text(exam["category"], language_code)
    frequency = translate_text(exam.get("frequency", tr("check_notice", language_code)), language_code)
    logo_text = escape(exam.get("logoText", make_exam_logo_text(exam)))
    st.markdown(
        f"""
        <div class="eh-card eh-exam-card" style="--accent: {accent}; --accent-bg: {accent}18;">
            <div class="eh-exam-header">
                <div class="eh-exam-logo" aria-label="{escape(exam["name"])} logo">{logo_text}</div>
                <div class="eh-exam-title-block">
                    <div class="eh-pill-row" style="margin: 0 0 12px;">
                        <span class="eh-pill eh-category-pill">{escape(category)}</span>
                        <span class="eh-pill">{escape(frequency)}</span>
                    </div>
                    <h3>{escape(translate_text(exam["name"], language_code))}</h3>
                </div>
            </div>
            <p>{escape(translate_text(exam["description"], language_code))}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    overview_tab, syllabus_tab, prep_tab, apply_tab = st.tabs(
        [
            tr("overview", language_code),
            tr("syllabus", language_code),
            tr("preparation", language_code),
            tr("apply", language_code),
        ]
    )

    with overview_tab:
        check_notice = tr("check_notice", language_code)
        check_latest = tr("check_latest", language_code)
        overview_panels = [
            render_overview_panel(
                tr("eligibility", language_code),
                translate_text(exam["eligibility"], language_code),
            ),
            render_overview_panel(tr("exam_pattern", language_code), translate_text(exam["pattern"], language_code)),
            render_overview_panel(
                tr("conducted_by", language_code),
                translate_text(exam.get("conductedBy", check_notice), language_code),
            ),
            render_overview_panel(
                tr("frequency", language_code),
                translate_text(exam.get("frequency", check_notice), language_code),
            ),
            render_overview_panel(
                tr("exam_mode", language_code),
                translate_text(exam.get("examMode", check_notice), language_code),
            ),
            render_overview_panel(
                tr("duration", language_code),
                translate_text(exam.get("duration", check_notice), language_code),
            ),
            render_overview_panel(
                tr("application_mode", language_code),
                translate_text(exam.get("applicationMode", check_notice), language_code),
            ),
            render_overview_panel(
                tr("fee", language_code),
                translate_text(exam.get("fee", check_latest), language_code),
            ),
            render_overview_panel(
                tr("used_for", language_code),
                translate_text(exam["useFor"], language_code),
                wide=True,
            ),
        ]
        st.markdown(
            f'<div class="eh-info-grid">{"".join(overview_panels)}</div>',
            unsafe_allow_html=True,
        )
        render_section_title("important_dates", language_code)
        st.table(
            {
                tr("stage", language_code): [
                    tr("notification", language_code),
                    tr("exam_date", language_code),
                ],
                tr("timeline", language_code): [
                    translate_text(
                        exam["dates"].get("notification", tr("to_be_announced", language_code)),
                        language_code,
                    ),
                    translate_text(
                        exam["dates"].get("examDate", tr("to_be_announced", language_code)),
                        language_code,
                    ),
                ],
            }
        )

    with syllabus_tab:
        render_section_title("syllabus_focus", language_code)
        st.markdown(
            '<div class="eh-chip-list">'
            + "".join(
                f'<span class="eh-pill">{escape(translate_text(item, language_code))}</span>'
                for item in exam["syllabus"]
            )
            + "</div>",
            unsafe_allow_html=True,
        )
        render_section_title("selection_process", language_code)
        st.markdown(
            '<div class="eh-timeline">'
            + "".join(
                f'<div class="eh-step"><strong>{index:02d}</strong> {escape(step)}</div>'
                for index, step in enumerate(
                    [translate_text(step, language_code) for step in exam["selectionProcess"]],
                    start=1,
                )
            )
            + "</div>",
            unsafe_allow_html=True,
        )

    with prep_tab:
        render_section_title("recommended_books", language_code)
        for book in exam["books"]:
            render_book_card(book, language_code)
        render_section_title("preparation_tips", language_code)
        for tip in exam["preparationTips"]:
            st.markdown(f"- {translate_text(tip, language_code)}")
        render_section_title("pyq", language_code)
        for paper in exam["pyq"]:
            st.link_button(f"{paper['year']} Question Paper", paper["url"])

    with apply_tab:
        render_section_title("application_mode", language_code)
        st.write(translate_text(exam.get("applicationMode", tr("check_latest", language_code)), language_code))
        render_section_title("fee", language_code)
        st.write(translate_text(exam.get("fee", tr("check_latest", language_code)), language_code))
        if exam.get("officialWebsite"):
            st.link_button(tr("official_website", language_code), exam["officialWebsite"])
        render_section_title("how_apply", language_code)
        for index, step in enumerate(exam["applicationSteps"], start=1):
            st.write(f"{index}. {translate_text(step, language_code)}")


def main():  # pragma: no cover
    st.set_page_config(page_title="Exam Hub", page_icon="EH", layout="wide")
    inject_theme()
    st.session_state.setdefault("selected_exam_id", None)

    exams = load_exams()
    categories = ["All categories"] + sorted({exam["category"] for exam in exams})

    with st.sidebar:
        st.markdown(
            """
            <div class="eh-sidebar-brand">
                <div class="eh-sidebar-logo">EH</div>
                <div class="eh-sidebar-name">Exam Hub</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        language_name = st.selectbox("Language", list(LANGUAGES), index=0)
        language_code = LANGUAGES[language_name]
        st.caption(tr("app_tagline", language_code))
        query = st.text_input(tr("search_exams", language_code), placeholder="GMAT, NEET, UPSC, JEE").strip().lower()
        category = st.selectbox(tr("category", language_code), categories)
        st.metric(tr("total_exams", language_code), len(exams))
        st.metric(tr("categories", language_code), len(categories) - 1)

    filtered_exams = [exam for exam in exams if matches_filters(exam, query, category)]

    render_hero(language_code)
    render_stat_grid(exams, filtered_exams, categories, language_code)

    render_section_title("matching_exams", language_code)
    visible_exams = filtered_exams[:9]
    for row_start in range(0, len(visible_exams), 3):
        preview_columns = st.columns(3)
        for column, exam in zip(preview_columns, visible_exams[row_start : row_start + 3], strict=False):
            with column:
                render_exam_preview(exam, language_code)
                if st.button(
                    tr("view_details", language_code),
                    key=f"open_exam_{exam['id']}",
                    type="primary",
                    use_container_width=True,
                ):
                    st.session_state.selected_exam_id = exam["id"]

    st.caption(f"{len(filtered_exams)} {tr('results', language_code)}{'s' if len(filtered_exams) != 1 else ''}")
    if not filtered_exams:
        st.session_state.selected_exam_id = None
        st.info(tr("no_results", language_code))
        return

    selected_exam = next(
        (exam for exam in filtered_exams if exam["id"] == st.session_state.selected_exam_id),
        None,
    )

    if selected_exam is None:
        st.info(tr("select_prompt", language_code))
        return

    render_exam_dialog(selected_exam, language_code)


if __name__ == "__main__":
    main()
