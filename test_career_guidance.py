"""
Automated Test Suite for AI-Powered Career Guidance System
Validates matching engine, skill-gap analysis, 30-day roadmap generation,
SQLite database persistence, and AI helper fallback resilience.
"""

import os
import sys
import unittest
import tempfile

# Ensure workspace root is in path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from career_data import CAREER_CATALOGUE
from recommender import match_careers
from roadmap import analyze_skill_gap, generate_30_day_roadmap
from database import init_db, save_assessment, get_all_assessments, get_assessment_by_id, delete_assessment
from ai_helper import generate_ai_career_explanation, ask_ai_career_assistant, is_ai_available


class TestCareerGuidanceSystem(unittest.TestCase):

    def setUp(self):
        self.sample_profile = {
            "name": "Alex",
            "degree_branch": "B.Tech / B.E. - Artificial Intelligence & Machine Learning (AIML)",
            "semester": 5,
            "interests": ["Problem Solving", "AI & Machine Learning", "Mathematics & Statistics"],
            "skills": ["Python", "SQL", "Statistics & Probability"],
            "subjects_enjoyed": ["Programming & Algorithms", "Statistics & Probability", "Machine Learning"],
            "work_style": "Analytical & Research-Oriented"
        }

    def test_career_catalogue_contains_8_careers(self):
        """Confirm catalogue contains exactly the 8 required careers with all fields."""
        expected_careers = [
            "Data Analyst",
            "Data Scientist",
            "ML Engineer",
            "AI Application Developer",
            "Cybersecurity Analyst",
            "Software Developer",
            "UI/UX Designer",
            "Cloud Engineer"
        ]
        self.assertEqual(len(CAREER_CATALOGUE), 8)
        for name in expected_careers:
            self.assertIn(name, CAREER_CATALOGUE)
            item = CAREER_CATALOGUE[name]
            self.assertIn("description", item)
            self.assertIn("required_skills", item)
            self.assertIn("beginner_learning_topics", item)
            self.assertIn("starter_project", item)
            self.assertIn("tech_stack", item["starter_project"])

    def test_recommender_returns_top_3_with_explanations(self):
        """Verify recommender outputs 3 sorted matches with non-empty reasons."""
        matches = match_careers(self.sample_profile, top_n=3)
        self.assertEqual(len(matches), 3)

        # Check sorting: highest match score first
        self.assertGreaterEqual(matches[0]["match_score"], matches[1]["match_score"])
        self.assertGreaterEqual(matches[1]["match_score"], matches[2]["match_score"])

        # Check each match has required transparent explanation fields
        for m in matches:
            self.assertIn("title", m)
            self.assertIn("match_score", m)
            self.assertIn("reasons", m)
            self.assertGreater(len(m["reasons"]), 0)
            self.assertIn("starter_project", m)

    def test_skill_gap_analysis_and_change_on_skill_removal(self):
        """Verify that removing a skill dynamically alters the skill gap list."""
        initial_skills = ["Python", "SQL", "Statistics & Probability"]
        gap_initial = analyze_skill_gap(initial_skills, "Data Scientist")

        self.assertIn("Python", gap_initial["acquired"])
        self.assertIn("Statistics & Probability", gap_initial["acquired"])
        self.assertIn("Machine Learning", gap_initial["missing"])

        # Remove Python and verify it moves from acquired to missing
        reduced_skills = ["SQL", "Statistics & Probability"]
        gap_reduced = analyze_skill_gap(reduced_skills, "Data Scientist")

        self.assertNotIn("Python", gap_reduced["acquired"])
        self.assertIn("Python", gap_reduced["missing"])
        self.assertLess(gap_reduced["readiness_pct"], gap_initial["readiness_pct"])

    def test_roadmap_structure_and_achievable_tasks(self):
        """Verify the 30-day roadmap contains 4 weeks, goals, milestones, and starter project."""
        roadmap = generate_30_day_roadmap(self.sample_profile, "Data Scientist")

        self.assertEqual(len(roadmap["weeks"]), 4)
        for i, week in enumerate(roadmap["weeks"]):
            self.assertEqual(week["week_number"], i + 1)
            self.assertTrue(len(week["goal"]) > 0)
            self.assertTrue(len(week["milestone"]) > 0)
            self.assertGreaterEqual(len(week["tasks"]), 3)

        self.assertIn("starter_project", roadmap)
        self.assertIn("title", roadmap["starter_project"])
        self.assertIn("tech_stack", roadmap["starter_project"])

    def test_database_persistence_and_retrieval(self):
        """Verify SQLite saving, retrieval by ID, list, and deletion with parameterized queries."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
            tmp_db = tmp.name

        try:
            self.assertTrue(init_db(tmp_db))
            matches = match_careers(self.sample_profile, top_n=3)

            # Save assessment
            record_id = save_assessment(self.sample_profile, matches, db_path=tmp_db)
            self.assertGreater(record_id, 0)

            # Retrieve all assessments
            records = get_all_assessments(db_path=tmp_db)
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["student_name"], "Alex")
            self.assertEqual(records[0]["top_career"], matches[0]["title"])

            # Retrieve by specific ID
            details = get_assessment_by_id(record_id, db_path=tmp_db)
            self.assertEqual(details["id"], record_id)
            self.assertEqual(details["degree_branch"], self.sample_profile["degree_branch"])
            self.assertIsInstance(details["skills"], list)
            self.assertIn("Python", details["skills"])

            # Delete assessment
            self.assertTrue(delete_assessment(record_id, db_path=tmp_db))
            remaining = get_all_assessments(db_path=tmp_db)
            self.assertEqual(len(remaining), 0)

        finally:
            if os.path.exists(tmp_db):
                try:
                    os.remove(tmp_db)
                except OSError:
                    pass

    def test_ai_helper_demo_mode_fallback_without_crash(self):
        """Verify that AI helper functions cleanly execute in Demo Mode without crashing."""
        matches = match_careers(self.sample_profile, top_n=3)

        # Test explanation generation (uses fallback if no key)
        explanation = generate_ai_career_explanation(self.sample_profile, matches)
        self.assertIn("status", explanation)
        self.assertIn("text", explanation)
        self.assertTrue(len(explanation["text"]) > 50)

        # Test AI assistant Q&A
        answer = ask_ai_career_assistant(self.sample_profile, matches[0]["title"], "How should I structure my resume?")
        self.assertIsInstance(answer, str)
        self.assertGreater(len(answer), 20)

    def test_ai_helper_handles_invalid_key_gracefully(self):
        """Verify that an invalid API key triggers a graceful fallback instead of an unhandled crash."""
        old_key = os.environ.get("GEMINI_API_KEY")
        try:
            os.environ["GEMINI_API_KEY"] = "invalid_fake_key_12345"
            matches = match_careers(self.sample_profile, top_n=3)

            explanation = generate_ai_career_explanation(self.sample_profile, matches)
            self.assertIn(explanation["status"], ["fallback", "success"])
            self.assertTrue(len(explanation["text"]) > 50)

            ans = ask_ai_career_assistant(self.sample_profile, matches[0]["title"], "How should I prepare for technical interviews?")
            self.assertIsInstance(ans, str)
            self.assertTrue("Interview Preparation" in ans or "career" in ans.lower())
        finally:
            if old_key is not None:
                os.environ["GEMINI_API_KEY"] = old_key
            elif "GEMINI_API_KEY" in os.environ:
                del os.environ["GEMINI_API_KEY"]

    def test_all_catalogue_careers_generate_valid_roadmaps(self):
        """Ensure every career in the catalogue generates a complete 4-week roadmap and skill gap."""
        for career_name in CAREER_CATALOGUE:
            gap = analyze_skill_gap(self.sample_profile["skills"], career_name)
            self.assertIn("acquired", gap)
            self.assertIn("missing", gap)
            self.assertIn("readiness_pct", gap)

            roadmap = generate_30_day_roadmap(self.sample_profile, career_name)
            self.assertEqual(len(roadmap["weeks"]), 4)
            self.assertIn("starter_project", roadmap)
            self.assertIn("title", roadmap["starter_project"])

    def test_custom_skills_matching(self):
        """Ensure custom entered skills are normalized and counted during matching."""
        profile_with_custom = self.sample_profile.copy()
        profile_with_custom["skills"] = ["Python", "SQL", "Pandas", "Scikit-Learn"]
        matches = match_careers(profile_with_custom, top_n=3)

        titles = [m["title"] for m in matches]
        self.assertIn("Data Scientist", titles)

    def test_gitignore_protects_secrets_and_database(self):
        """Ensure .env and *.db are specified in .gitignore."""
        gitignore_path = os.path.join(PARENT_DIR, ".gitignore")
        self.assertTrue(os.path.exists(gitignore_path))
        with open(gitignore_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn(".env", content)
        self.assertIn(".venv", content)
        self.assertIn("career_guidance.db", content)


if __name__ == "__main__":
    unittest.main()
