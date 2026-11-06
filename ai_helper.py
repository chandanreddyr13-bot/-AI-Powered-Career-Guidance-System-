"""
AI Helper for AI-Powered Career Guidance System
Interfaces with Google Gen AI SDK (Gemini API) to generate personalized explanations,
actionable 30-day advice, and answer follow-up student questions.
Includes 100% reliable DEMO MODE fallback when no API key is provided or network is offline.
"""

import os
import json
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

def get_api_key() -> str:
    """Retrieve Gemini API key from environment safely without logging it."""
    return os.getenv("GEMINI_API_KEY", "").strip()


def is_ai_available() -> bool:
    """Check if a Gemini API key is configured in the environment."""
    return bool(get_api_key())


def _build_demo_explanation(student_profile: dict, top_careers: list) -> str:
    """
    Generate an insightful, deterministic rule-based explanation when running in Demo Mode.
    Ensures zero crashes and full hackathon presentation readiness.
    """
    name = student_profile.get("name") or "Student"
    degree = student_profile.get("degree_branch", "Technical Degree")
    interests = student_profile.get("interests", [])
    skills = student_profile.get("skills", [])

    top1 = top_careers[0] if len(top_careers) > 0 else None
    top2 = top_careers[1] if len(top_careers) > 1 else None
    top3 = top_careers[2] if len(top_careers) > 2 else None

    if not top1:
        return "Please complete your profile to view personalized career guidance."

    text = f"""### 💡 Career Evaluation for {name} ({degree})

Based on your unique combination of interests in **{', '.join(interests[:3]) if interests else 'technology'}** and existing skills in **{', '.join(skills[:3]) if skills else 'foundational concepts'}**, here is how your top recommendations align:

1. **Top Recommendation: {top1['title']} (Match: {top1['match_score']}%)**
   - **Why this fits you**: You already possess foundational familiarity with {len(top1['matched_skills'])} relevant skill(s) ({', '.join(top1['matched_skills']) if top1['matched_skills'] else 'core concepts'}).
   - **Key Advantage**: Your strong alignment with {top1['category']} allows you to transition theoretical coursework into practical portfolio evidence.
   - **Immediate Focus**: Prioritize mastering `{', '.join(top1['missing_skills'][:2]) if top1['missing_skills'] else 'advanced architecture'}` over the next 30 days.

2. **Strong Alternative: {top2['title'] if top2 else 'Secondary Option'} (Match: {top2['match_score'] if top2 else 0}%)**
   - Offers an excellent complementary path, particularly if you want to broaden into `{top2['category'] if top2 else 'related fields'}`.

3. **Emerging Horizon: {top3['title'] if top3 else 'Tertiary Option'} (Match: {top3['match_score'] if top3 else 0}%)**
   - A high-growth specialization that builds on your logical problem-solving foundation.

> ℹ️ *Generated in Hackathon Demo Mode using transparent rule-based heuristics. Add a GEMINI_API_KEY to `.env` to enable real-time generative responses.*
"""
    return text.strip()


def generate_ai_career_explanation(student_profile: dict, top_careers: list) -> dict:
    """
    Generate clear, personalized explanation of the recommendations.
    Uses Google Gen AI SDK if key is available; otherwise gracefully falls back to Demo Mode.
    """
    api_key = get_api_key()

    if not api_key:
        return {
            "source": "demo_mode",
            "text": _build_demo_explanation(student_profile, top_careers),
            "status": "success"
        }

    try:
        from google import genai

        client = genai.Client(api_key=api_key)

        prompt = f"""
You are an encouraging, expert university career counselor and technical mentor.
Analyze the following student profile and the already computed top 3 career matches.
Explain in clear, friendly, and practical language why these career paths fit the student,
highlight their greatest strengths, and provide actionable advice for their next 30 days.
Avoid promising guaranteed jobs, high salaries, or making unrealistic claims.

Student Profile:
- Degree / Branch: {student_profile.get('degree_branch')}
- Semester: {student_profile.get('semester')}
- Key Interests: {', '.join(student_profile.get('interests', []))}
- Current Skills: {', '.join(student_profile.get('skills', []))}
- Favorite Subjects: {', '.join(student_profile.get('subjects_enjoyed', []))}
- Preferred Work Style: {student_profile.get('work_style')}

Top Career Matches (Computed by rule-based match score):
1. {top_careers[0]['title']} (Score: {top_careers[0]['match_score']}%) - Reasons: {'; '.join(top_careers[0].get('reasons', []))}
2. {top_careers[1]['title'] if len(top_careers) > 1 else 'N/A'} (Score: {top_careers[1]['match_score'] if len(top_careers) > 1 else 0}%)
3. {top_careers[2]['title'] if len(top_careers) > 2 else 'N/A'} (Score: {top_careers[2]['match_score'] if len(top_careers) > 2 else 0}%)

Format your response in friendly Markdown with:
1. Executive Summary & Strengths
2. Detailed breakdown of why Match #1 is an ideal fit
3. Quick perspective on Alternatives (#2 and #3)
4. Strategic advice for their 30-day learning sprint
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return {
            "source": "gemini_ai",
            "text": response.text,
            "status": "success"
        }

    except Exception as e:
        # Graceful fallback on any API error (quota, network, invalid key)
        fallback_text = _build_demo_explanation(student_profile, top_careers)
        return {
            "source": "demo_mode_fallback",
            "text": f"{fallback_text}\n\n*(Notice: Live AI temporarily unavailable: {str(e)[:80]}. Demo fallback displayed.)*",
            "status": "fallback"
        }


def _get_offline_assistant_response(student_profile: dict, target_career: str, user_question: str) -> str:
    """
    Generate a high-quality offline rule-based response for common career queries.
    Provides immediate answers for resume, interview, scheduling, and general questions.
    """
    q_lower = user_question.lower()
    skills = student_profile.get('skills', [])

    if "resume" in q_lower or "cv" in q_lower:
        return (
            f"**Resume Advice for {target_career}:**\n\n"
            f"1. **Highlight Projects Over Coursework**: Feature your starter project with a GitHub link, "
            f"explaining the problem, stack used, and metrics.\n"
            f"2. **Group Technical Skills**: Categorize skills into Languages ({', '.join(skills[:2]) if skills else 'Python'}), "
            f"Tools & Frameworks, and Core Fundamentals.\n"
            f"3. **Keep it 1 Page**: Use clean single-column bullet points with quantifiable actions."
        )
    elif "interview" in q_lower or "questions" in q_lower:
        return (
            f"**Interview Preparation for {target_career}:**\n\n"
            f"1. **Core Fundamentals**: Expect questions on core data structures, syntax, and foundational concepts.\n"
            f"2. **Project Walkthrough**: Be prepared to explain architectural choices, trade-offs, and bugs you overcame in your projects.\n"
            f"3. **Problem Solving**: Practice explaining your thought process out loud before writing code."
        )
    elif "time" in q_lower or "hours" in q_lower or "schedule" in q_lower:
        return (
            f"**Balancing Study Time for {target_career}:**\n\n"
            "Aim for **45 to 60 minutes each weekday** and a **2-hour focused weekend session** (~6 hours/week). "
            "Consistency is far more effective than weekend cramming. Focus on one topic at a time."
        )
    else:
        return (
            f"**Career Guidance for {target_career}:**\n\n"
            f"Regarding *'{user_question}'*:\n\n"
            f"As an undergraduate student with interests in {', '.join(student_profile.get('interests', [])[:2])}, "
            f"your best next step toward **{target_career}** is to complete the 4-week structured roadmap, "
            f"build the starter portfolio project, and share your progress openly on GitHub or LinkedIn.\n\n"
            f"> *(Demo Mode: Add a GEMINI_API_KEY to `.env` to unlock open-ended conversational AI answers).* "
        )


def ask_ai_career_assistant(student_profile: dict, target_career: str, user_question: str) -> str:
    """
    Conversational assistant that answers follow-up career questions grounded
    in the student's profile and target career path.
    """
    api_key = get_api_key()

    if not api_key:
        return _get_offline_assistant_response(student_profile, target_career, user_question)

    try:
        from google import genai
        client = genai.Client(api_key=api_key)

        prompt = f"""
You are an expert technical career mentor. The student is asking a follow-up question.
Provide a concise, practical, honest, and encouraging response tailored to their specific background.

Student Background:
- Degree & Semester: {student_profile.get('degree_branch')}, Sem {student_profile.get('semester')}
- Target Career Path: {target_career}
- Current Skills: {', '.join(student_profile.get('skills', []))}
- Key Interests: {', '.join(student_profile.get('interests', []))}

Student Question: "{user_question}"

Keep the answer under 200 words, direct, structured with bullet points where appropriate, and actionable.
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        fallback = _get_offline_assistant_response(student_profile, target_career, user_question)
        return f"{fallback}\n\n*(Notice: Live AI temporarily unavailable: {str(e)[:80]}. Showing offline demo guidance.)*"
