"""
Recommender Engine for AI-Powered Career Guidance System
Calculates a transparent, rule-based matching score between student profiles
and the curated career catalogue. Returns top 3 recommendations with clear explanations.
"""

from career_data import CAREER_CATALOGUE


def _normalize_string(s: str) -> str:
    """Normalize strings for case-insensitive and whitespace-tolerant comparison."""
    return s.strip().lower()


def _calculate_overlap_ratio(student_items, career_items):
    """
    Compute overlap ratio between student selections and career requirements.
    Matches substrings or exact strings to be tolerant of phrasing variations.
    """
    if not career_items:
        return 0.0, []

    matched = []
    norm_student = [_normalize_string(x) for x in student_items if x]

    for c_item in career_items:
        norm_c = _normalize_string(c_item)
        # Check direct or partial inclusion
        for s_item in norm_student:
            if s_item in norm_c or norm_c in s_item:
                matched.append(c_item)
                break

    # Avoid duplicate matches
    matched = list(dict.fromkeys(matched))
    ratio = len(matched) / len(career_items)
    return min(1.0, ratio), matched


def match_careers(student_profile: dict, top_n: int = 3) -> list:
    """
    Calculate transparent match scores across all careers in the catalogue.

    Weights used:
    - Interests Overlap: 40%
    - Skills Overlap: 35%
    - Enjoyed Subjects Overlap: 15%
    - Preferred Work Style Alignment: 10%

    Returns a list of dicts for the top_n careers, sorted by match_score descending.
    """
    interests = student_profile.get("interests", [])
    skills = student_profile.get("skills", [])
    subjects = student_profile.get("subjects_enjoyed", [])
    work_style = student_profile.get("work_style", "")

    scored_careers = []

    for career_key, career in CAREER_CATALOGUE.items():
        # 1. Interests Overlap (Weight: 40%)
        interest_ratio, matched_interests = _calculate_overlap_ratio(
            interests, career["relevant_interests"]
        )

        # 2. Skills Overlap (Weight: 35%)
        skill_ratio, matched_skills = _calculate_overlap_ratio(
            skills, career["required_skills"]
        )

        # 3. Subjects Overlap (Weight: 15%)
        subject_ratio, matched_subjects = _calculate_overlap_ratio(
            subjects, career["enjoyed_subjects"]
        )

        # 4. Work Style Alignment (Weight: 10%)
        work_style_ratio = 0.0
        norm_work_style = _normalize_string(work_style) if work_style else ""
        for pref in career["preferred_work_styles"]:
            if norm_work_style and norm_work_style in _normalize_string(pref):
                work_style_ratio = 1.0
                break

        # Calculate weighted match score (0 - 100%)
        raw_score = (
            (0.40 * interest_ratio) +
            (0.35 * skill_ratio) +
            (0.15 * subject_ratio) +
            (0.10 * work_style_ratio)
        ) * 100

        # Scale score to a practical, realistic range (minimum baseline for non-zero matches)
        match_score = round(raw_score, 1)

        # Identify missing skills that need to be learned
        missing_skills = [
            skill for skill in career["required_skills"]
            if skill not in matched_skills
        ]

        # Generate transparent reasoning
        reasons = []
        if matched_interests:
            reasons.append(
                f"Matches {len(matched_interests)} of your key interests: "
                f"{', '.join(matched_interests[:3])}."
            )
        if matched_skills:
            reasons.append(
                f"You already possess {len(matched_skills)} core prerequisite skills: "
                f"{', '.join(matched_skills)}."
            )
        else:
            reasons.append(
                "Fresh path with high potential based on your declared interests and coursework."
            )
        if matched_subjects:
            reasons.append(
                f"Aligns with your favorite subjects: {', '.join(matched_subjects[:2])}."
            )
        if work_style_ratio > 0:
            reasons.append(
                f"Fits your preferred work style: '{work_style}'."
            )

        scored_careers.append({
            "title": career["title"],
            "category": career["category"],
            "description": career["description"],
            "match_score": match_score,
            "matched_interests": matched_interests,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "matched_subjects": matched_subjects,
            "reasons": reasons,
            "starter_project": career["starter_project"],
            "beginner_learning_topics": career["beginner_learning_topics"],
            "required_skills": career["required_skills"],
            "breakdown": {
                "interests_overlap_pct": round(interest_ratio * 100, 1),
                "skills_overlap_pct": round(skill_ratio * 100, 1),
                "subjects_overlap_pct": round(subject_ratio * 100, 1),
                "work_style_match": bool(work_style_ratio > 0)
            }
        })

    # Sort descending by match score
    scored_careers.sort(key=lambda x: x["match_score"], reverse=True)

    return scored_careers[:top_n]
