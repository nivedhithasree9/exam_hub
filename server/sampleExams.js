function pyqs(prefix) {
  return Array.from({ length: 2 }).map((_, i) => {
    const year = 2025 - i;
    const slug = prefix.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    return {
      year,
      title: `${prefix} ${year}`,
      url: `https://www.google.com/search?q=${encodeURIComponent(`${prefix} ${year} previous year question paper pdf`)}`,
      file: `/papers/${slug}-${year}.pdf`
    };
  });
}

const extraDetails = {
  'Joint Entrance Examination (JEE Advanced)': {
    conductedBy: 'One of the IITs on a rotating basis under JAB',
    frequency: 'Once a year',
    applicationMode: 'Online',
    examMode: 'Computer-based test',
    duration: 'Two papers of 3 hours each',
    markingScheme: 'Varies by question type; may include negative marking',
    fee: 'Varies by category and nationality',
    officialWebsite: 'https://jeeadv.ac.in',
    selectionProcess: ['Qualify JEE Main', 'Register for JEE Advanced', 'Appear for both papers', 'Participate in JoSAA counselling'],
    useFor: 'Admission to IIT undergraduate engineering and science programs',
    preparationTips: ['Revise JEE Main concepts deeply', 'Practice mixed-subject problems', 'Solve previous IIT papers', 'Take full-length mock tests']
  },
  'Joint Entrance Examination (JEE Main)': {
    conductedBy: 'National Testing Agency (NTA)',
    frequency: 'Usually twice a year',
    applicationMode: 'Online',
    examMode: 'Computer-based test',
    duration: '3 hours',
    markingScheme: '+4 for correct answer and -1 for incorrect MCQ',
    fee: 'Varies by category, paper, and exam city',
    officialWebsite: 'https://jeemain.nta.nic.in',
    selectionProcess: ['Apply online', 'Appear for JEE Main', 'Use score for NIT/IIIT/GFTI admission', 'Top candidates qualify for JEE Advanced'],
    useFor: 'Admission to NITs, IIITs, GFTIs, and eligibility for JEE Advanced',
    preparationTips: ['Master NCERT Chemistry', 'Practice numerical problems daily', 'Analyze mock test mistakes', 'Revise formulas frequently']
  },
  'National Eligibility cum Entrance Test (NEET UG)': {
    conductedBy: 'National Testing Agency (NTA)',
    frequency: 'Once a year',
    applicationMode: 'Online',
    examMode: 'Offline pen-and-paper test',
    duration: '3 hours 20 minutes',
    markingScheme: '+4 for correct answer and -1 for incorrect answer',
    fee: 'Varies by category and exam center location',
    officialWebsite: 'https://neet.nta.nic.in',
    selectionProcess: ['Apply online', 'Appear for NEET UG', 'Check rank and score', 'Participate in medical counselling'],
    useFor: 'Admission to MBBS, BDS, AYUSH, and other medical programs',
    preparationTips: ['Read NCERT Biology line by line', 'Practice Physics numericals', 'Revise reactions and formulas', 'Attempt timed mock tests']
  },
  'Graduate Aptitude Test in Engineering (GATE)': {
    conductedBy: 'IISc/IITs on a rotating basis',
    frequency: 'Once a year',
    applicationMode: 'Online',
    examMode: 'Computer-based test',
    duration: '3 hours',
    markingScheme: 'Question-dependent; MCQs may include negative marking',
    fee: 'Varies by category and application timing',
    officialWebsite: 'https://gate2026.iitg.ac.in',
    selectionProcess: ['Apply for selected paper', 'Appear for GATE', 'Use score for M.Tech/PhD admissions or PSU applications'],
    useFor: 'M.Tech admissions, research programs, and PSU recruitment',
    preparationTips: ['Finish core subjects first', 'Revise Engineering Mathematics', 'Practice previous papers', 'Make short revision notes']
  },
  'Common Admission Test (CAT)': {
    conductedBy: 'Indian Institutes of Management (IIMs)',
    frequency: 'Once a year',
    applicationMode: 'Online',
    examMode: 'Computer-based test',
    duration: 'About 2 hours',
    markingScheme: '+3 for correct answer; negative marking for wrong MCQs',
    fee: 'Varies by category',
    officialWebsite: 'https://iimcat.ac.in',
    selectionProcess: ['Register for CAT', 'Appear for exam', 'Shortlisting by institutes', 'WAT/GD/PI or interview rounds'],
    useFor: 'MBA/PGDM admission to IIMs and many business schools',
    preparationTips: ['Read daily for VARC', 'Practice DILR sets', 'Build arithmetic speed', 'Take sectional mocks']
  },
  'Union Public Service Commission (UPSC) CSE': {
    conductedBy: 'Union Public Service Commission',
    frequency: 'Once a year',
    applicationMode: 'Online',
    examMode: 'Offline written exam and interview',
    duration: 'Multiple papers across Prelims and Mains',
    markingScheme: 'Prelims objective; Mains descriptive; interview/personality test',
    fee: 'Varies by category; many categories are exempt',
    officialWebsite: 'https://upsc.gov.in',
    selectionProcess: ['Preliminary exam', 'Main examination', 'Personality test', 'Final merit list'],
    useFor: 'Recruitment to IAS, IPS, IFS, IRS, and other central services',
    preparationTips: ['Read NCERTs and standard books', 'Follow current affairs', 'Practice answer writing', 'Revise syllabus repeatedly']
  },
  'Staff Selection Commission (SSC) CGL': {
    conductedBy: 'Staff Selection Commission',
    frequency: 'Once a year',
    applicationMode: 'Online',
    examMode: 'Computer-based test',
    duration: 'Varies by tier',
    markingScheme: 'Objective papers with negative marking',
    fee: 'Varies by category; many categories are exempt',
    officialWebsite: 'https://ssc.gov.in',
    selectionProcess: ['Tier I', 'Tier II', 'Document verification', 'Final allocation'],
    useFor: 'Central government Group B and Group C posts',
    preparationTips: ['Practice arithmetic daily', 'Revise current affairs', 'Improve English grammar', 'Solve previous SSC papers']
  },
  'SSC Combined Higher Secondary Level (SSC CHSL)': {
    conductedBy: 'Staff Selection Commission',
    frequency: 'Once a year',
    applicationMode: 'Online',
    examMode: 'Computer-based test',
    duration: 'Varies by tier',
    markingScheme: 'Objective test with negative marking',
    fee: 'Varies by category; many categories are exempt',
    officialWebsite: 'https://ssc.gov.in',
    selectionProcess: ['Tier I', 'Tier II', 'Skill/typing test where applicable', 'Document verification'],
    useFor: 'Recruitment to LDC, JSA, PA, SA, and DEO posts',
    preparationTips: ['Build typing speed if required', 'Practice reasoning sets', 'Revise grammar rules', 'Attempt timed mocks']
  },
  'Institute of Banking Personnel Selection PO (IBPS PO)': {
    conductedBy: 'Institute of Banking Personnel Selection',
    frequency: 'Once a year',
    applicationMode: 'Online',
    examMode: 'Computer-based test',
    duration: 'Prelims and Mains have separate durations',
    markingScheme: 'Objective tests with negative marking',
    fee: 'Varies by category',
    officialWebsite: 'https://www.ibps.in',
    selectionProcess: ['Preliminary exam', 'Main exam', 'Interview', 'Provisional allotment'],
    useFor: 'Probationary Officer recruitment in public sector banks',
    preparationTips: ['Practice speed maths', 'Read banking awareness', 'Solve puzzles daily', 'Improve reading comprehension']
  },
  'State Bank of India PO (SBI PO)': {
    conductedBy: 'State Bank of India',
    frequency: 'Usually once a year',
    applicationMode: 'Online',
    examMode: 'Computer-based test',
    duration: 'Prelims and Mains have separate durations',
    markingScheme: 'Objective sections with negative marking',
    fee: 'Varies by category',
    officialWebsite: 'https://sbi.co.in/web/careers',
    selectionProcess: ['Preliminary exam', 'Main exam', 'Psychometric test', 'Group exercise and interview'],
    useFor: 'Probationary Officer recruitment in SBI',
    preparationTips: ['Focus on data analysis', 'Practice high-level reasoning', 'Revise banking and economy', 'Take full mocks']
  },
  'Railway Recruitment Board NTPC (RRB NTPC)': {
    conductedBy: 'Railway Recruitment Boards',
    frequency: 'As per railway recruitment cycle',
    applicationMode: 'Online',
    examMode: 'Computer-based test',
    duration: 'Varies by stage',
    markingScheme: 'Objective questions with negative marking',
    fee: 'Varies by category',
    officialWebsite: 'https://www.rrbcdg.gov.in',
    selectionProcess: ['CBT 1', 'CBT 2', 'Skill/typing test where applicable', 'Document verification and medical exam'],
    useFor: 'Non-technical posts in Indian Railways',
    preparationTips: ['Practice basic maths', 'Read railway/general awareness', 'Solve CBT papers', 'Improve accuracy under time limits']
  },
  'Common Law Admission Test (CLAT)': {
    conductedBy: 'Consortium of National Law Universities',
    frequency: 'Once a year',
    applicationMode: 'Online',
    examMode: 'Offline pen-and-paper test',
    duration: '2 hours',
    markingScheme: '+1 for correct answer and negative marking for wrong answer',
    fee: 'Varies by category',
    officialWebsite: 'https://consortiumofnlus.ac.in',
    selectionProcess: ['Apply online', 'Appear for CLAT', 'Check rank', 'Participate in NLU counselling'],
    useFor: 'Admission to law programs at National Law Universities',
    preparationTips: ['Read editorials daily', 'Practice legal reasoning passages', 'Revise current affairs', 'Solve mock papers']
  },
  'National Defence Academy (NDA)': {
    conductedBy: 'Union Public Service Commission',
    frequency: 'Twice a year',
    applicationMode: 'Online',
    examMode: 'Offline written exam and SSB interview',
    duration: 'Written exam followed by multi-day SSB process',
    markingScheme: 'Objective written papers with negative marking',
    fee: 'Varies by category; many candidates are exempt',
    officialWebsite: 'https://upsc.gov.in',
    selectionProcess: ['Written exam', 'SSB interview', 'Medical examination', 'Final merit list'],
    useFor: 'Admission to NDA and Naval Academy programs',
    preparationTips: ['Practice mathematics thoroughly', 'Read current affairs', 'Prepare for SSB communication tasks', 'Maintain physical fitness']
  },
  'Central Teacher Eligibility Test (CTET)': {
    conductedBy: 'Central Board of Secondary Education',
    frequency: 'Usually twice a year',
    applicationMode: 'Online',
    examMode: 'Computer-based or offline depending on notification',
    duration: '2 hours 30 minutes per paper',
    markingScheme: 'No negative marking',
    fee: 'Varies by category and number of papers',
    officialWebsite: 'https://ctet.nic.in',
    selectionProcess: ['Apply online', 'Appear for Paper I/Paper II', 'Obtain qualifying score', 'Use certificate for teacher recruitment'],
    useFor: 'Teacher eligibility for central government schools and related recruitment',
    preparationTips: ['Understand pedagogy concepts', 'Practice previous papers', 'Revise NCERT basics', 'Focus on child development']
  },
  'University Grants Commission NET (UGC NET)': {
    conductedBy: 'National Testing Agency on behalf of UGC',
    frequency: 'Usually twice a year',
    applicationMode: 'Online',
    examMode: 'Computer-based test',
    duration: '3 hours',
    markingScheme: '+2 for each correct answer; no negative marking',
    fee: 'Varies by category',
    officialWebsite: 'https://ugcnet.nta.nic.in',
    selectionProcess: ['Apply online', 'Appear for Paper I and Paper II', 'Qualify for Assistant Professor/JRF based on cutoff'],
    useFor: 'Assistant Professor eligibility and Junior Research Fellowship',
    preparationTips: ['Master Paper I concepts', 'Revise subject syllabus deeply', 'Practice PYQs', 'Track recent research/current developments']
  }
};

function enrichExam(exam) {
  return {
    ...exam,
    ...(extraDetails[exam.name] || {}),
    applicationSteps: [
      'Visit the official exam website and open the latest notification.',
      'Create an account or sign in with your registered email/mobile number.',
      'Fill personal, educational, category, and exam-city details carefully.',
      'Upload photograph, signature, and required certificates in the specified format.',
      'Pay the application fee if applicable and save the payment receipt.',
      'Download the submitted application form and keep it for future reference.'
    ]
  };
}

const sampleExams = [
  {
    name: 'Joint Entrance Examination (JEE Advanced)',
    category: 'Engineering',
    description: 'National level engineering entrance exam for IIT admissions',
    eligibility: 'Qualified JEE Main and passed 10+2 with Physics, Chemistry, and Mathematics',
    syllabus: ['Physics', 'Chemistry', 'Mathematics'],
    pattern: 'Two computer-based papers with numerical and objective questions',
    books: [
      'Physics: Concepts of Physics Vol. 1 & 2 - H.C. Verma',
      'Physics: Problems in General Physics - I.E. Irodov',
      'Chemistry: NCERT Class 11 & 12 Chemistry',
      'Mathematics: Cengage JEE Advanced Mathematics series'
    ],
    pyq: pyqs('JEE Advanced'),
    dates: { notification: 'April', examDate: 'June' }
  },
  {
    name: 'Joint Entrance Examination (JEE Main)',
    category: 'Engineering',
    description: 'Entrance exam for NITs, IIITs, GFTIs, and JEE Advanced qualification',
    eligibility: 'Passed or appearing in 10+2 with Physics, Chemistry, and Mathematics',
    syllabus: ['Physics', 'Chemistry', 'Mathematics'],
    pattern: 'Computer-based test with MCQs and numerical value questions',
    books: [
      'Physics: Concepts of Physics Vol. 1 & 2 - H.C. Verma',
      'Chemistry: NCERT Class 11 & 12 Chemistry',
      'Mathematics: Objective Mathematics for JEE - R.D. Sharma',
      'Practice: Arihant JEE Main Previous Years Solved Papers'
    ],
    pyq: pyqs('JEE Main'),
    dates: { notification: 'November', examDate: 'January / April' }
  },
  {
    name: 'National Eligibility cum Entrance Test (NEET UG)',
    category: 'Medical',
    description: 'Medical entrance exam for MBBS, BDS, and allied undergraduate courses',
    eligibility: '10+2 with Physics, Chemistry, Biology/Biotechnology, and English',
    syllabus: ['Physics', 'Chemistry', 'Botany', 'Zoology'],
    pattern: 'Offline objective exam based on NCERT syllabus',
    books: [
      'Biology: NCERT Class 11 & 12 Biology',
      'Biology Practice: MTG Objective NCERT at Your Fingertips',
      'Physics: Concepts of Physics - H.C. Verma',
      'Chemistry: NCERT Chemistry with MTG/Arihant practice questions'
    ],
    pyq: pyqs('NEET UG'),
    dates: { notification: 'February', examDate: 'May' }
  },
  {
    name: 'Graduate Aptitude Test in Engineering (GATE)',
    category: 'Engineering',
    description: 'Postgraduate engineering entrance and PSU recruitment exam',
    eligibility: 'Engineering, science, architecture, or relevant degree students/graduates',
    syllabus: ['Core engineering subject', 'Engineering Mathematics', 'General Aptitude'],
    pattern: 'Computer-based test with MCQ, MSQ, and numerical answer questions',
    books: [
      'Core Subject: Made Easy GATE study package',
      'Core Subject: ACE Academy GATE material',
      'Engineering Mathematics: Made Easy Engineering Mathematics',
      'Practice: GATE previous year solved papers by Made Easy/Ace Academy'
    ],
    pyq: pyqs('GATE'),
    dates: { notification: 'August', examDate: 'February' }
  },
  {
    name: 'Common Admission Test (CAT)',
    category: 'Management',
    description: 'MBA entrance exam for IIMs and other business schools',
    eligibility: 'Bachelor degree with required minimum marks',
    syllabus: ['VARC', 'DILR', 'Quantitative Aptitude'],
    pattern: 'Computer-based test with sectional time limits',
    books: [
      'Quantitative Aptitude: How to Prepare for Quantitative Aptitude - Arun Sharma',
      'DILR: How to Prepare for Data Interpretation & Logical Reasoning - Arun Sharma',
      'VARC: Word Power Made Easy - Norman Lewis',
      'Practice: CAT previous year papers and IMS/TIME/CL mock tests'
    ],
    pyq: pyqs('CAT'),
    dates: { notification: 'July', examDate: 'November' }
  },
  {
    name: 'Union Public Service Commission (UPSC) CSE',
    category: 'Government',
    description: 'Civil services exam for IAS, IPS, IFS, and allied services',
    eligibility: 'Graduation from a recognized university',
    syllabus: ['General Studies', 'CSAT', 'Optional subject', 'Essay'],
    pattern: 'Prelims, Mains, and Interview',
    books: [
      'Polity: Indian Polity - M. Laxmikanth',
      'Geography: Certificate Physical and Human Geography - G.C. Leong',
      'History: Spectrum Modern India - Rajiv Ahir',
      'Economy: Indian Economy - Ramesh Singh',
      'Current Affairs: The Hindu/Indian Express plus monthly current affairs magazine'
    ],
    pyq: pyqs('UPSC CSE'),
    dates: { notification: 'February', examDate: 'May' }
  },
  {
    name: 'Staff Selection Commission (SSC) CGL',
    category: 'Government',
    description: 'Graduate level recruitment for central government ministries and departments',
    eligibility: 'Graduation from a recognized university',
    syllabus: ['Quantitative Aptitude', 'Reasoning', 'English', 'General Awareness'],
    pattern: 'Tiered computer-based examinations',
    books: [
      'Quantitative Aptitude: R.S. Aggarwal or Kiran SSC Maths',
      'Reasoning: A Modern Approach to Verbal & Non-Verbal Reasoning - R.S. Aggarwal',
      'English: Objective General English - S.P. Bakshi',
      'General Awareness: Lucent General Knowledge',
      'Practice: Kiran SSC CGL previous year solved papers'
    ],
    pyq: pyqs('SSC CGL'),
    dates: { notification: 'June', examDate: 'September' }
  },
  {
    name: 'SSC Combined Higher Secondary Level (SSC CHSL)',
    category: 'Government',
    description: 'Recruitment exam for LDC, JSA, PA, SA, and DEO posts',
    eligibility: 'Passed 10+2 from a recognized board',
    syllabus: ['Reasoning', 'Quantitative Aptitude', 'English', 'General Awareness'],
    pattern: 'Tier I objective test followed by Tier II skill/descriptive stages',
    books: [
      'Practice: Kiran SSC CHSL previous year solved papers',
      'English: Objective General English - S.P. Bakshi',
      'Maths: Fast Track Objective Arithmetic - Rajesh Verma',
      'Reasoning: R.S. Aggarwal Verbal & Non-Verbal Reasoning',
      'General Awareness: Lucent General Knowledge'
    ],
    pyq: pyqs('SSC CHSL'),
    dates: { notification: 'April', examDate: 'July' }
  },
  {
    name: 'Institute of Banking Personnel Selection PO (IBPS PO)',
    category: 'Banking',
    description: 'Probationary Officer recruitment exam for public sector banks',
    eligibility: 'Graduation from a recognized university',
    syllabus: ['Reasoning', 'Quantitative Aptitude', 'English', 'Banking Awareness'],
    pattern: 'Prelims, Mains, and Interview',
    books: [
      'Banking Awareness: Arihant Banking Awareness',
      'Quantitative Aptitude: Fast Track Objective Arithmetic - Rajesh Verma',
      'Reasoning: A Modern Approach to Verbal & Non-Verbal Reasoning - R.S. Aggarwal',
      'English: Word Power Made Easy - Norman Lewis',
      'Practice: Oliveboard/Testbook/BankersAdda mock tests'
    ],
    pyq: pyqs('IBPS PO'),
    dates: { notification: 'August', examDate: 'October' }
  },
  {
    name: 'State Bank of India PO (SBI PO)',
    category: 'Banking',
    description: 'Probationary Officer recruitment exam for State Bank of India',
    eligibility: 'Graduation from a recognized university',
    syllabus: ['Reasoning', 'Data Analysis', 'English', 'General Economy Banking Awareness'],
    pattern: 'Prelims, Mains, psychometric test, group exercise, and interview',
    books: [
      'Practice: SBI PO previous year solved papers',
      'Reasoning: A Modern Approach to Verbal & Non-Verbal Reasoning - R.S. Aggarwal',
      'Quant/Data Analysis: Quantum CAT - Sarvesh K. Verma',
      'Banking Awareness: Arihant Banking Awareness',
      'Mock Tests: Oliveboard/PracticeMock SBI PO test series'
    ],
    pyq: pyqs('SBI PO'),
    dates: { notification: 'September', examDate: 'November' }
  },
  {
    name: 'Railway Recruitment Board NTPC (RRB NTPC)',
    category: 'Railways',
    description: 'Recruitment exam for non-technical popular categories in Indian Railways',
    eligibility: '10+2 or graduation depending on the post',
    syllabus: ['Mathematics', 'General Intelligence', 'General Awareness'],
    pattern: 'CBT 1, CBT 2, skill/typing test where applicable',
    books: [
      'General Awareness: Lucent General Knowledge',
      'Practice: Kiran RRB NTPC solved papers',
      'Mathematics: Fast Track Objective Arithmetic - Rajesh Verma',
      'Reasoning: R.S. Aggarwal Verbal & Non-Verbal Reasoning',
      'Current Affairs: Monthly railway/general awareness magazine'
    ],
    pyq: pyqs('RRB NTPC'),
    dates: { notification: 'To be announced', examDate: 'To be announced' }
  },
  {
    name: 'Common Law Admission Test (CLAT)',
    category: 'Law',
    description: 'Entrance exam for undergraduate and postgraduate law programs at NLUs',
    eligibility: '10+2 for UG law programs; LLB for PG law programs',
    syllabus: ['English', 'Current Affairs', 'Legal Reasoning', 'Logical Reasoning', 'Quantitative Techniques'],
    pattern: 'Offline comprehension-based objective test',
    books: [
      'Legal Reasoning: Legal Awareness and Legal Reasoning - A.P. Bhardwaj',
      'English: Word Power Made Easy - Norman Lewis',
      'Current Affairs: Manorama Yearbook plus monthly current affairs',
      'Practice: Universal/LexisNexis CLAT previous year papers',
      'Mock Tests: Career Launcher/LegalEdge CLAT mocks'
    ],
    pyq: pyqs('CLAT'),
    dates: { notification: 'July', examDate: 'December' }
  },
  {
    name: 'National Defence Academy (NDA)',
    category: 'Defence',
    description: 'UPSC exam for admission to Army, Navy, and Air Force wings of NDA',
    eligibility: '10+2; Physics and Mathematics required for Air Force and Navy',
    syllabus: ['Mathematics', 'General Ability Test', 'English', 'General Knowledge'],
    pattern: 'Written exam followed by SSB interview',
    books: [
      'Complete Guide: Pathfinder NDA/NA - Arihant',
      'Mathematics: NCERT Class 11 & 12 Mathematics',
      'General Knowledge: Lucent General Knowledge',
      'English: Objective General English - S.P. Bakshi',
      'Practice: NDA previous year solved papers by Arihant'
    ],
    pyq: pyqs('NDA'),
    dates: { notification: 'December / May', examDate: 'April / September' }
  },
  {
    name: 'Central Teacher Eligibility Test (CTET)',
    category: 'Teaching',
    description: 'Eligibility test for teaching positions in central government schools',
    eligibility: 'Teacher training qualification as per paper level',
    syllabus: ['Child Development', 'Language I', 'Language II', 'Mathematics', 'Environmental Studies'],
    pattern: 'Objective paper for primary and elementary teaching levels',
    books: [
      'Complete Guide: Arihant CTET Paper I & II',
      'Pedagogy: Child Development and Pedagogy - Disha/Arihant',
      'School Concepts: NCERT textbooks Class 1 to 8',
      'Practice: CTET previous year solved papers',
      'Mock Tests: Disha/Oswaal CTET practice sets'
    ],
    pyq: pyqs('CTET'),
    dates: { notification: 'March / September', examDate: 'July / December' }
  },
  {
    name: 'University Grants Commission NET (UGC NET)',
    category: 'Teaching',
    description: 'Eligibility exam for Assistant Professor and Junior Research Fellowship',
    eligibility: 'Postgraduate degree with required minimum marks',
    syllabus: ['Teaching and Research Aptitude', 'Subject-specific paper'],
    pattern: 'Computer-based test with two objective papers',
    books: [
      'Paper I: Trueman UGC NET/SET General Paper',
      'Paper I: NTA UGC NET Paper I by Arihant',
      'Subject Paper: Trueman/Arihant subject-specific guide',
      'Practice: NTA UGC NET previous year papers',
      'Mock Tests: NTA official mock tests and practice sets'
    ],
    pyq: pyqs('UGC NET'),
    dates: { notification: 'April / September', examDate: 'June / December' }
  }
].map(enrichExam);

module.exports = sampleExams;
