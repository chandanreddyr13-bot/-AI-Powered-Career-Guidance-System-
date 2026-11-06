"""
Career Data Catalogue for AI-Powered Career Guidance System
Contains an editable, beginner-friendly catalogue of 8 prominent technology career paths.
"""

CAREER_CATALOGUE = {
    "Data Analyst": {
        "title": "Data Analyst",
        "category": "Data & Analytics",
        "description": "Transforms raw business and operational data into clear visualizations, actionable reports, and metric dashboards to drive decision-making.",
        "relevant_interests": [
            "Data Analysis",
            "Business Intelligence",
            "Statistics",
            "Problem Solving",
            "Storytelling with Data"
        ],
        "required_skills": [
            "SQL",
            "Python",
            "Data Visualization",
            "Excel / Spreadsheets",
            "Statistics & Probability",
            "Tableau or Power BI"
        ],
        "enjoyed_subjects": [
            "Statistics & Probability",
            "Database Systems",
            "Mathematics",
            "Business Analytics"
        ],
        "preferred_work_styles": [
            "Analytical & Research-Oriented",
            "Detail-Oriented & Methodical",
            "Collaborative & Business-Facing"
        ],
        "beginner_learning_topics": [
            "SQL fundamentals: SELECT, JOINs, GROUP BY, and aggregate window functions",
            "Exploratory Data Analysis (EDA) using Python (Pandas and Matplotlib)",
            "Data cleaning and missing value imputation strategies",
            "Building interactive dashboards in Tableau, Power BI, or Streamlit",
            "Descriptive statistics: Mean, Variance, Correlation, and Percentiles"
        ],
        "starter_project": {
            "title": "E-Commerce Customer Insights & Sales Dashboard",
            "objective": "Clean a raw retail transactions dataset, analyze customer purchasing trends, and build an interactive visualization dashboard.",
            "tech_stack": "Python, Pandas, Streamlit, SQL",
            "weekly_milestones": [
                "Week 1: Write SQL queries to extract summary statistics from sales tables.",
                "Week 2: Perform data cleaning and compute Key Performance Indicators (Average Order Value, Retention Rate).",
                "Week 3: Build interactive charts showing revenue by category and monthly trends.",
                "Week 4: Assemble a polished Streamlit dashboard and publish on GitHub."
            ]
        }
    },
    "Data Scientist": {
        "title": "Data Scientist",
        "category": "Data & Analytics",
        "description": "Applies statistical modeling, exploratory experiments, and machine learning algorithms to uncover patterns and predict future trends.",
        "relevant_interests": [
            "Machine Learning",
            "Mathematics & Statistics",
            "Data Analysis",
            "Research & Experimentation",
            "Problem Solving"
        ],
        "required_skills": [
            "Python",
            "Statistics & Probability",
            "Machine Learning",
            "SQL",
            "Scikit-Learn",
            "Data Cleaning & Feature Engineering"
        ],
        "enjoyed_subjects": [
            "Statistics & Probability",
            "Linear Algebra & Calculus",
            "Machine Learning",
            "Database Systems"
        ],
        "preferred_work_styles": [
            "Analytical & Research-Oriented",
            "Curious & Experimental",
            "Independent & Deep-Focus"
        ],
        "beginner_learning_topics": [
            "Statistical hypothesis testing, distributions, and p-values",
            "Supervised learning: Linear Regression, Logistic Regression, Decision Trees",
            "Feature engineering, scaling, and categorical encoding",
            "Model evaluation metrics: Accuracy, Precision, Recall, F1-Score, ROC-AUC",
            "Reproducible research workflows using Jupyter notebooks and Git"
        ],
        "starter_project": {
            "title": "Student Academic Outcome & Churn Predictor",
            "objective": "Build and evaluate an end-to-end predictive machine learning model that forecasts student completion probabilities.",
            "tech_stack": "Python, Scikit-Learn, Pandas, Matplotlib",
            "weekly_milestones": [
                "Week 1: Conduct exploratory data analysis on student demographic and grade records.",
                "Week 2: Engineer features and prepare train-test data splits with cross-validation.",
                "Week 3: Train Random Forest and Logistic Regression models; compare evaluation metrics.",
                "Week 4: Write a model evaluation report documenting feature importances and caveats."
            ]
        }
    },
    "ML Engineer": {
        "title": "ML Engineer",
        "category": "AI & Systems Engineering",
        "description": "Bridges the gap between data science prototypes and production software, designing automated training pipelines and scalable model serving systems.",
        "relevant_interests": [
            "Machine Learning",
            "AI & Systems",
            "Software Architecture",
            "Model Deployment",
            "High Performance Computing"
        ],
        "required_skills": [
            "Python",
            "Machine Learning",
            "Deep Learning Basics",
            "Docker / Containerization",
            "REST APIs (FastAPI / Flask)",
            "Git & Version Control"
        ],
        "enjoyed_subjects": [
            "Programming & Algorithms",
            "Operating Systems",
            "Machine Learning",
            "Computer Architecture"
        ],
        "preferred_work_styles": [
            "Hands-on Coding & Building Systems",
            "Systematic & Production-Minded",
            "Analytical & Research-Oriented"
        ],
        "beginner_learning_topics": [
            "Packaging ML models with joblib/pickle and creating inference scripts",
            "Building high-throughput REST APIs using FastAPI",
            "Containerizing Python microservices with Docker",
            "Model registry and versioning fundamentals",
            "Basic Deep Learning with PyTorch or TensorFlow"
        ],
        "starter_project": {
            "title": "Containerized Text Classification Microservice",
            "objective": "Train a lightweight NLP classifier, wrap it with a FastAPI endpoint, and package it into a runnable Docker container.",
            "tech_stack": "Python, FastAPI, Scikit-Learn, Docker",
            "weekly_milestones": [
                "Week 1: Train and export a text sentiment classification pipeline.",
                "Week 2: Create a FastAPI REST endpoint with Pydantic request validation.",
                "Week 3: Write automated unit tests for API endpoints and error handling.",
                "Week 4: Build a Dockerfile, test container execution locally, and document API specs."
            ]
        }
    },
    "AI Application Developer": {
        "title": "AI Application Developer",
        "category": "Modern AI & Web",
        "description": "Integrates foundation models, LLM APIs, and vector search into intelligent user-facing applications that solve everyday business problems.",
        "relevant_interests": [
            "AI & Machine Learning",
            "Generative AI & LLMs",
            "Web Application Development",
            "Prompt Engineering",
            "Problem Solving"
        ],
        "required_skills": [
            "Python",
            "LLM APIs (e.g., Gemini API)",
            "Prompt Engineering",
            "Streamlit / Web Frameworks",
            "REST APIs",
            "Git & Version Control"
        ],
        "enjoyed_subjects": [
            "Programming & Software Design",
            "Human-Computer Interaction",
            "Artificial Intelligence",
            "Web Technologies"
        ],
        "preferred_work_styles": [
            "Hands-on Coding & Building Systems",
            "Creative & Solution-Driven",
            "Fast Prototyping & Iteration"
        ],
        "beginner_learning_topics": [
            "Calling modern generative AI APIs (e.g. Google Gen AI SDK)",
            "Structured prompt design and system instruction tuning",
            "Building interactive web frontends rapidly with Streamlit",
            "Handling API errors, rate limits, and fallback strategies",
            "Basics of Retrieval-Augmented Generation (RAG) and document querying"
        ],
        "starter_project": {
            "title": "AI-Powered Course Notes Summarizer & Quiz Generator",
            "objective": "Build a responsive web application where students paste lecture notes to receive key takeaway summaries and practice flashcard quizzes.",
            "tech_stack": "Python, Streamlit, Google Gen AI SDK",
            "weekly_milestones": [
                "Week 1: Set up Gemini API client, test prompt templates, and parse responses.",
                "Week 2: Build Streamlit interface for text input and structured output formatting.",
                "Week 3: Add export options (Markdown notes) and implement graceful offline fallback.",
                "Week 4: Test edge cases, refine prompts, and publish live on Streamlit Community Cloud."
            ]
        }
    },
    "Cybersecurity Analyst": {
        "title": "Cybersecurity Analyst",
        "category": "Security & Infrastructure",
        "description": "Monitors networks, identifies vulnerabilities, audits software configurations, and defends organizational systems against cyber threats.",
        "relevant_interests": [
            "Security & System Protection",
            "Ethical Hacking",
            "Computer Networks",
            "Investigation & Forensic Analysis",
            "Linux Systems"
        ],
        "required_skills": [
            "Computer Networks & Protocols",
            "Linux Basics",
            "Network Analysis (Wireshark / Nmap)",
            "Security Principles (CIA Triad)",
            "Python or Bash Scripting"
        ],
        "enjoyed_subjects": [
            "Computer Networks",
            "Operating Systems",
            "Information & Network Security",
            "Discrete Mathematics"
        ],
        "preferred_work_styles": [
            "Security & System Protection",
            "Methodical & Detail-Oriented",
            "Investigative & Cautious"
        ],
        "beginner_learning_topics": [
            "TCP/IP, UDP, DNS, HTTP/S, and OSI 7-layer networking models",
            "Linux terminal commands, permissions, and service management",
            "Port scanning and vulnerability reconnaissance with Nmap",
            "OWASP Top 10 web application security risks",
            "Basics of cryptography: Hashing, symmetric vs asymmetric encryption"
        ],
        "starter_project": {
            "title": "Automated Local Network Port & Vulnerability Auditor",
            "objective": "Develop a lightweight Python script that scans local open ports, flags insecure services, and compiles an audit security checklist.",
            "tech_stack": "Python, Socket Programming, Linux, Markdown",
            "weekly_milestones": [
                "Week 1: Study TCP socket connection mechanics and write a basic port probe.",
                "Week 2: Map open ports to standard service vulnerabilities (FTP, Telnet, HTTP).",
                "Week 3: Add banner grabbing and format findings into an automated report.",
                "Week 4: Document defensive remediation steps and upload to GitHub."
            ]
        }
    },
    "Software Developer": {
        "title": "Software Developer",
        "category": "Software Engineering",
        "description": "Designs, writes, tests, and maintains robust software systems, backend APIs, and web services that solve concrete user needs.",
        "relevant_interests": [
            "Hands-on Coding & Building Systems",
            "Algorithm Design",
            "Web Development",
            "Software Architecture",
            "Problem Solving"
        ],
        "required_skills": [
            "Python (or Java/C++)",
            "Data Structures & Algorithms",
            "Git & Version Control",
            "SQL & Relational Databases",
            "REST API Development",
            "Object-Oriented Programming"
        ],
        "enjoyed_subjects": [
            "Data Structures & Algorithms",
            "Object-Oriented Programming",
            "Database Management Systems",
            "Software Engineering"
        ],
        "preferred_work_styles": [
            "Hands-on Coding & Building Systems",
            "Logical & Structured",
            "Collaborative Team Player"
        ],
        "beginner_learning_topics": [
            "Object-Oriented Design principles (Classes, Inheritance, Modular code)",
            "Time and space complexity (Big-O) analysis of core data structures",
            "Building RESTful CRUD endpoints with automated routing",
            "Relational database modeling with schema constraints and foreign keys",
            "Writing unit tests and setting up continuous integration workflows"
        ],
        "starter_project": {
            "title": "Full-Stack Task & Project Management API",
            "objective": "Create a robust backend service managing users, tasks, and deadlines with parameterized database queries and clean REST endpoints.",
            "tech_stack": "Python, FastAPI/Flask, SQLite, Pytest",
            "weekly_milestones": [
                "Week 1: Design database schema (Users, Tasks, Categories) and set up SQLite migrations.",
                "Week 2: Implement CRUD endpoints with request validation and status codes.",
                "Week 3: Write comprehensive unit and integration tests using Pytest.",
                "Week 4: Document API with OpenAPI/Swagger and publish clean repository."
            ]
        }
    },
    "UI/UX Designer": {
        "title": "UI/UX Designer",
        "category": "Design & Product",
        "description": "Designs accessible, intuitive, and visually compelling digital interfaces based on user research, wireframes, and interactive prototypes.",
        "relevant_interests": [
            "Creative & User-Centered",
            "Visual Design & Aesthetics",
            "Human-Computer Interaction",
            "User Research & Empathy",
            "Prototyping & Wireframing"
        ],
        "required_skills": [
            "Figma / Wireframing Tools",
            "UI Design Principles & Typography",
            "User Research & Personas",
            "HTML / CSS Basics",
            "Prototyping & Usability Testing"
        ],
        "enjoyed_subjects": [
            "Human-Computer Interaction",
            "Web Technologies",
            "Psychology / Product Design",
            "Software Engineering"
        ],
        "preferred_work_styles": [
            "Creative & User-Centered",
            "Empathetic & Visual",
            "Collaborative & Iterative"
        ],
        "beginner_learning_topics": [
            "Visual hierarchy: Typography scales, color contrast, and spacing systems",
            "Figma mastery: Auto-layout, components, variants, and interactive links",
            "User research methods: Interviews, user journey mapping, and empathy maps",
            "Designing accessible interfaces complying with WCAG guidelines",
            "Translating UI wireframes into responsive HTML/CSS structures"
        ],
        "starter_project": {
            "title": "Mobile Student Habit & Wellness App Prototype",
            "objective": "Conduct mini user research, design wireframes, and build a high-fidelity interactive clickable Figma prototype with a design system.",
            "tech_stack": "Figma, User Journey Maps, WCAG Accessibility Guidelines",
            "weekly_milestones": [
                "Week 1: Create user personas and draft low-fidelity paper wireframes.",
                "Week 2: Establish a Figma design system (Color palette, typography, button variants).",
                "Week 3: Build high-fidelity screens for onboarding, dashboard, and habit tracking.",
                "Week 4: Link interactive prototype interactions and prepare a case study presentation."
            ]
        }
    },
    "Cloud Engineer": {
        "title": "Cloud Engineer",
        "category": "Cloud & DevOps",
        "description": "Architects, configures, and automates reliable cloud infrastructure, storage buckets, compute instances, and CI/CD pipelines.",
        "relevant_interests": [
            "Infrastructure & Automation",
            "Cloud Computing",
            "Linux Systems",
            "System Reliability & DevOps",
            "Networking"
        ],
        "required_skills": [
            "Cloud Fundamentals (AWS / GCP / Azure)",
            "Linux & Shell Scripting",
            "Docker / Containers",
            "Networking (VPC, DNS, Subnets)",
            "Git & CI/CD Basics"
        ],
        "enjoyed_subjects": [
            "Operating Systems",
            "Computer Networks",
            "Distributed Systems",
            "Cloud Computing"
        ],
        "preferred_work_styles": [
            "Infrastructure & Automation",
            "Systematic & Production-Minded",
            "Problem Solving & Scaling"
        ],
        "beginner_learning_topics": [
            "Cloud service models (IaaS, PaaS, SaaS) and core provider services (Compute, Storage)",
            "Virtual Private Clouds (VPC), subnets, routing tables, and security groups",
            "Automating deployments using Bash scripts and Git webhooks",
            "Container lifecycle: building, tagging, and running Docker containers",
            "Identity and Access Management (IAM) least-privilege security policies"
        ],
        "starter_project": {
            "title": "Multi-Tier Web Application Cloud Deployment",
            "objective": "Deploy a containerized web application backed by cloud storage and automated GitHub Actions CI/CD deployment pipeline.",
            "tech_stack": "Docker, Linux, Cloud Platform (AWS/GCP), GitHub Actions",
            "weekly_milestones": [
                "Week 1: Configure Linux virtual server, SSH access, and firewall rules.",
                "Week 2: Containerize application frontend and backend with docker-compose.",
                "Week 3: Set up cloud storage bucket for static assets and configure domain routing.",
                "Week 4: Implement automated GitHub Actions workflow to build and deploy on push."
            ]
        }
    }
}

# Standard curated lists for UI dropdowns and selections
INTEREST_OPTIONS = [
    "Problem Solving",
    "AI & Machine Learning",
    "Generative AI & LLMs",
    "Data Analysis",
    "Mathematics & Statistics",
    "Hands-on Coding & Building Systems",
    "Web Development",
    "Cloud Computing",
    "Security & System Protection",
    "Ethical Hacking",
    "Linux Systems",
    "Creative & User-Centered",
    "Visual Design & Aesthetics",
    "Infrastructure & Automation",
    "Business Intelligence",
    "Research & Experimentation"
]

SKILL_OPTIONS = [
    "Python",
    "SQL",
    "JavaScript",
    "HTML / CSS",
    "Git & Version Control",
    "Data Structures & Algorithms",
    "Statistics & Probability",
    "Machine Learning",
    "Data Visualization",
    "Linux Basics",
    "Docker / Containers",
    "REST APIs",
    "Figma / Wireframing Tools",
    "Cloud Fundamentals (AWS / GCP / Azure)",
    "LLM APIs (e.g., Gemini API)",
    "Prompt Engineering",
    "Excel / Spreadsheets"
]

SUBJECT_OPTIONS = [
    "Programming & Algorithms",
    "Data Structures & Algorithms",
    "Database Systems",
    "Statistics & Probability",
    "Computer Networks",
    "Operating Systems",
    "Machine Learning",
    "Artificial Intelligence",
    "Software Engineering",
    "Human-Computer Interaction",
    "Object-Oriented Programming",
    "Cloud Computing",
    "Information & Network Security"
]

WORK_STYLE_OPTIONS = [
    "Analytical & Research-Oriented",
    "Hands-on Coding & Building Systems",
    "Creative & User-Centered",
    "Security & System Protection",
    "Infrastructure & Automation",
    "Collaborative Team Player",
    "Detail-Oriented & Methodical"
]

DEGREE_BRANCH_OPTIONS = [
    "B.Tech / B.E. - Artificial Intelligence & Machine Learning (AIML)",
    "B.Tech / B.E. - Computer Science & Engineering (CSE)",
    "B.Tech / B.E. - Information Technology (IT)",
    "B.Tech / B.E. - Data Science",
    "B.Tech / B.E. - Electronics & Communication (ECE)",
    "B.Tech / B.E. - Electrical & Electronics (EEE)",
    "B.Sc / M.Sc - Computer Science",
    "BCA / MCA - Computer Applications",
    "Other Engineering / Science Branch"
]
