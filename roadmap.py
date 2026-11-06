"""
Skill-Gap Analysis and 30-Day Learning Roadmap Generator
Produces structured, realistic, beginner-friendly 4-week study plans and starter project blueprints.
"""

from career_data import CAREER_CATALOGUE


def analyze_skill_gap(student_skills: list, career_title: str) -> dict:
    """
    Compare student skills with career requirements.
    Returns acquired skills, missing skills to learn, and readiness ratio.
    """
    career = CAREER_CATALOGUE.get(career_title)
    if not career:
        return {
            "acquired": [],
            "missing": [],
            "readiness_pct": 0.0,
            "total_required": 0
        }

    required = career["required_skills"]
    norm_student = [s.strip().lower() for s in student_skills if s]

    acquired = []
    missing = []

    for req in required:
        norm_req = req.strip().lower()
        if any(s in norm_req or norm_req in s for s in norm_student):
            acquired.append(req)
        else:
            missing.append(req)

    total = len(required)
    readiness_pct = round((len(acquired) / total * 100), 1) if total > 0 else 0.0

    return {
        "acquired": acquired,
        "missing": missing,
        "readiness_pct": readiness_pct,
        "total_required": total
    }


def generate_30_day_roadmap(student_profile: dict, career_title: str) -> dict:
    """
    Generate a realistic, beginner-friendly 30-day learning roadmap divided into 4 weeks.
    Customized dynamically based on the student's existing skills vs. missing skills.
    """
    career = CAREER_CATALOGUE.get(career_title)
    if not career:
        return {}

    student_skills = student_profile.get("skills", [])
    gap = analyze_skill_gap(student_skills, career_title)
    missing = gap["missing"]
    starter_project = career["starter_project"]
    learning_topics = career["beginner_learning_topics"]

    # Select primary missing topics to focus on
    focus_topic_1 = missing[0] if len(missing) > 0 else "Advanced Concepts"
    focus_topic_2 = missing[1] if len(missing) > 1 else (learning_topics[1] if len(learning_topics) > 1 else "Hands-on Practice")

    roadmap = {
        "career_title": career_title,
        "overview": (
            f"A realistic 30-day (4-week) study plan designed for undergraduate students. "
            f"Commitment: 5 to 7 hours per week alongside your coursework. "
            f"Focuses on closing skill gaps and assembling a verifiable starter project."
        ),
        "disclaimer": (
            "This roadmap is designed for self-paced skill exploration. "
            "It does not guarantee employment, academic credits, or immediate hiring."
        ),
        "weeks": [
            {
                "week_number": 1,
                "title": f"Week 1: Core Fundamentals & Essential Syntax ({focus_topic_1})",
                "goal": f"Establish a solid theoretical and syntax foundation in {focus_topic_1}.",
                "milestone": f"Write and run 5 small exercise scripts covering {focus_topic_1} basics.",
                "tasks": [
                    f"Complete beginner tutorials and interactive docs for {focus_topic_1}.",
                    f"Study: {learning_topics[0] if len(learning_topics) > 0 else 'Core fundamentals'}.",
                    "Set up your local development environment and Git repository.",
                    "Practice daily 45-minute coding drills to build muscle memory."
                ]
            },
            {
                "week_number": 2,
                "title": f"Week 2: Applied Tooling & Deep Dive ({focus_topic_2})",
                "goal": f"Apply core principles to realistic problem scenarios with {focus_topic_2}.",
                "milestone": "Build a functional mini-feature or mini-module demonstrating data handling.",
                "tasks": [
                    f"Explore standard libraries and best practices for {focus_topic_2}.",
                    f"Study: {learning_topics[1] if len(learning_topics) > 1 else 'Intermediate implementations'}.",
                    "Write error handling and input validation routines.",
                    "Review 2 open-source beginner repositories on GitHub to see idiomatic code structure."
                ]
            },
            {
                "week_number": 3,
                "title": "Week 3: Integration, Data Flow & Architecture",
                "goal": "Connect your individual modules into an end-to-end working system.",
                "milestone": "Complete the core logic and backend/frontend flow of your starter project.",
                "tasks": [
                    f"Study: {learning_topics[2] if len(learning_topics) > 2 else 'System integration'}.",
                    f"Begin development on '{starter_project['title']}'.",
                    "Implement the primary user input and output display pipeline.",
                    "Test edge cases and fix syntax or runtime bugs."
                ]
            },
            {
                "week_number": 4,
                "title": "Week 4: Portfolio Starter Project, Polish & Documentation",
                "goal": "Finalize your starter project, author a thorough README, and publish to GitHub.",
                "milestone": "A public GitHub repository with clean code, screenshots, and an explanatory README.",
                "tasks": [
                    f"Deliverable: Complete '{starter_project['title']}' ({starter_project['tech_stack']}).",
                    "Add documentation: installation guide, architecture diagram, and demo walkthrough.",
                    "Write unit tests or validation checks for core functions.",
                    "Share your project with a peer or mentor for constructive feedback."
                ]
            }
        ],
        "starter_project": starter_project
    }

    return roadmap
