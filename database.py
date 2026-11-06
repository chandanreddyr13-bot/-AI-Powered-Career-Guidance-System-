"""
Database Module for AI-Powered Career Guidance System
Manages local SQLite persistence for student assessment history and profiles.
Uses parameterized queries and robust error handling.
"""

import sqlite3
import json
import os
from datetime import datetime

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "career_guidance.db")


def get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Establish and return a SQLite database connection with row factory."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DEFAULT_DB_PATH) -> bool:
    """Initialize the SQLite database schema if it doesn't already exist."""
    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS saved_assessments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_name TEXT,
                    degree_branch TEXT NOT NULL,
                    semester INTEGER NOT NULL,
                    interests TEXT,
                    skills TEXT,
                    subjects_enjoyed TEXT,
                    work_style TEXT,
                    top_career TEXT NOT NULL,
                    top_match_score REAL NOT NULL,
                    recommendations_json TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"[DB ERROR] Failed to initialize database: {e}")
        return False


def save_assessment(student_profile: dict, top_careers: list, db_path: str = DEFAULT_DB_PATH) -> int:
    """
    Save an assessment result to SQLite.
    Only called when the user explicitly clicks the Save button.
    Returns the newly inserted row ID or -1 on error.
    """
    if not top_careers:
        return -1

    init_db(db_path)

    student_name = student_profile.get("name", "Anonymous Student") or "Anonymous Student"
    degree_branch = student_profile.get("degree_branch", "Technical Degree")
    semester = student_profile.get("semester", 1)
    interests_json = json.dumps(student_profile.get("interests", []))
    skills_json = json.dumps(student_profile.get("skills", []))
    subjects_json = json.dumps(student_profile.get("subjects_enjoyed", []))
    work_style = student_profile.get("work_style", "")

    top_career = top_careers[0]["title"]
    top_score = top_careers[0]["match_score"]
    recommendations_json = json.dumps(top_careers)

    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO saved_assessments (
                    student_name,
                    degree_branch,
                    semester,
                    interests,
                    skills,
                    subjects_enjoyed,
                    work_style,
                    top_career,
                    top_match_score,
                    recommendations_json,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student_name,
                degree_branch,
                semester,
                interests_json,
                skills_json,
                subjects_json,
                work_style,
                top_career,
                top_score,
                recommendations_json,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            conn.commit()
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"[DB ERROR] Failed to save assessment: {e}")
        return -1


def get_all_assessments(db_path: str = DEFAULT_DB_PATH) -> list:
    """Retrieve all saved assessments ordered by newest first."""
    init_db(db_path)
    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, student_name, degree_branch, semester, top_career, top_match_score, created_at
                FROM saved_assessments
                ORDER BY id DESC
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    except sqlite3.Error as e:
        print(f"[DB ERROR] Failed to fetch assessments: {e}")
        return []


def get_assessment_by_id(assessment_id: int, db_path: str = DEFAULT_DB_PATH) -> dict:
    """Retrieve a full saved assessment record by ID, parsing stored JSON fields."""
    init_db(db_path)
    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM saved_assessments WHERE id = ?
            """, (assessment_id,))
            row = cursor.fetchone()
            if not row:
                return {}

            data = dict(row)
            # Parse JSON fields safely
            for json_field in ["interests", "skills", "subjects_enjoyed", "recommendations_json"]:
                if data.get(json_field):
                    try:
                        data[json_field] = json.loads(data[json_field])
                    except json.JSONDecodeError:
                        pass
            return data
    except sqlite3.Error as e:
        print(f"[DB ERROR] Failed to fetch assessment #{assessment_id}: {e}")
        return {}


def delete_assessment(assessment_id: int, db_path: str = DEFAULT_DB_PATH) -> bool:
    """Delete a saved assessment record by ID."""
    init_db(db_path)
    try:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM saved_assessments WHERE id = ?", (assessment_id,))
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"[DB ERROR] Failed to delete assessment #{assessment_id}: {e}")
        return False
