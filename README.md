<<<<<<< HEAD
# AI-POWERED CAREER GUIDANCE SYSTEM 🧭
### *A Beginner-Friendly Hackathon MVP Built with Google Antigravity*

> **Project Goal**: Recommend suitable career paths, identify skill gaps, and generate a practical 30-day learning roadmap from a student's profile.

---

## 📌 Executive Summary

The **AI-Powered Career Guidance System** empowers undergraduate students to navigate career options based on their academic coursework, technical skills, interests, and preferred work styles.

Designed following the **Hackathon Build Guide**, the system combines:
1. **Transparent Rule-Based Matching**: Computes weighted overlap scores against an editable catalogue of 8 industry career paths without claiming unrealistic psychometric certainty.
2. **Dynamic Skill-Gap Analysis**: Compares a student's existing skills with prerequisites to highlight competencies to acquire next.
3. **Actionable 30-Day Learning Roadmap**: Formulates a realistic 4-week study sprint (5–7 hours/week) equipped with weekly milestones and a portfolio starter project blueprint.
4. **Google Gen AI (Gemini) Layer**: Translates technical alignment data into encouraging natural language career guidance and powers an interactive AI Career Assistant.
5. **Zero-Failure Demo Mode**: Operates seamlessly in hackathons even without internet or an API key via pre-computed deterministic fallbacks.
6. **SQLite Local Persistence**: Saves student profiles and recommendations safely using parameterized SQL queries.

---

## 🏗️ System Architecture

```
Student Profile Form
(Degree, Semester, Interests, Skills, Subjects, Work Style)
         │
         ▼
Transparent Recommender Engine (recommender.py)
   ├── Interests Overlap (40%)
   ├── Skills Overlap (35%)
   ├── Subjects Enjoyed (15%)
   └── Work Style Alignment (10%)
         │
         ├─────────────────────────────────────────┐
         ▼                                         ▼
Top 3 Career Recommendations               Skill-Gap Analyzer (roadmap.py)
         │                                         │
         ▼                                         ▼
AI Explanation Layer (ai_helper.py)        30-Day Action Roadmap & Starter Project
  - Gemini API / Demo Mode Fallback                │
         │                                         │
         └───────────────────┬─────────────────────┘
                             ▼
                 Streamlit Web Application (app.py)
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   SQLite Database (database.py)      Markdown Roadmap Export
```

---

## 📂 Project Structure

```
CareerGuidanceAI/
├── app.py                   # Streamlit web dashboard & multi-page navigation
├── career_data.py           # Catalogue of 8 career paths & domain taxonomies
├── recommender.py           # Transparent weighted rule-based matching engine
├── roadmap.py               # Skill-gap analyzer & 4-week learning roadmap generator
├── database.py              # SQLite storage with parameterized queries
├── ai_helper.py             # Google Gen AI (Gemini) SDK integration & Demo Mode
├── run_career_guidance.bat  # One-click launcher for Windows
├── requirements.txt         # Project dependencies (Streamlit, python-dotenv, google-genai)
├── .env.example             # Template for optional Gemini API key
├── .gitignore               # Configured to ignore secrets (.env), .venv, and SQLite DBs
├── tests/
│   └── test_career_guidance.py # Automated unit test suite (7 comprehensive tests)
└── README.md                # Project documentation & Hackathon Pitch Guide
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites & Environment Setup
Ensure Python 3.11+ is installed. Then open PowerShell or terminal in the project directory:

```powershell
# Create virtual environment
py -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1
# (or run directly using .\.venv\Scripts\python.exe)
```

### 2. Install Dependencies
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. (Optional) Configure Gemini API Key
The application includes a resilient **Hackathon Demo Mode** that functions completely without an API key. To unlock live generative responses:
1. Copy `.env.example` to `.env`:
   ```powershell
   copy .env.example .env
   ```
2. Open `.env` and set your key:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key
   ```

### 4. Run the Application
```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```
Or simply double-click `run_career_guidance.bat`.

---

## 🧪 Running Automated Tests

Run the test suite to verify matching, skill gap analysis, roadmaps, and database operations:

```powershell
.\.venv\Scripts\python.exe -m unittest tests/test_career_guidance.py
```
*Expected Output:*
```
Ran 7 tests in 0.045s
OK
```

---

## 🎤 Hackathon 2-Minute Presentation Script

| Time | Phase | Script & Action |
|---|---|---|
| **0:00 - 0:20** | **The Problem** | *"Engineering and tech students face choice overload. With dozens of emerging specializations, they struggle to identify which roles genuinely match their coursework and skills, and they lack a structured roadmap to bridge their gaps."* |
| **0:20 - 0:50** | **Live Input** | Click **'⚡ Fill Sample Demo Profile'** in the dashboard. *"We collect high-level student profile preferences—without asking for intrusive personal data like phone numbers or passwords."* |
| **0:50 - 1:20** | **Recommendations & Skill Gap** | Click **'Generate Career Recommendations'**. *"Our transparent matching engine evaluates 8 tech paths and highlights the Top 3 matches (e.g. Data Scientist at 84%). Switching to the Skill-Gap tab immediately shows which skills the student already has versus the critical gaps to learn next."* |
| **1:20 - 1:45** | **Roadmap & Starter Project** | *"Instead of vague advice, we provide a realistic 30-day plan split into 4 achievable weeks (5–7 hrs/week) capped with an end-to-end starter portfolio project."* |
| **1:45 - 2:00** | **AI Layer & Closing** | Show the AI evaluation and SQLite save feature. *"Powered by Google Gen AI with a resilient offline fallback, this tool empowers informed student exploration while emphasizing that AI assists, but does not replace, qualified mentorship."* |

---

## 🛡️ Responsible AI & Ethical Design
- **Transparent Heuristics**: Match scores are calculated via open, verifiable overlap metrics rather than opaque black-box models.
- **Privacy by Design**: No telephone numbers, physical addresses, passwords, or government IDs are collected or stored.
- **Safe Fallbacks**: API exceptions or offline environments trigger structured heuristic explanations rather than crashing.
- **Realistic Framing**: The application explicitly avoids making guarantees regarding admissions, job offers, or salary projections.
=======
# -AI-Powered-Career-Guidance-System-
>>>>>>> 05a697b810fdefd3e8833b225ad9990e4697ca25
