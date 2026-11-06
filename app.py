"""
AI-Powered Career Guidance System
Streamlit Web Application for Hackathon MVP
"""

import os
import sys
import json
import streamlit as st

# Page Configuration MUST be the first Streamlit command
st.set_page_config(
    page_title="CareerGuidanceAI - AI-Powered Career Guidance System",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Local module imports
from career_data import (
    CAREER_CATALOGUE,
    INTEREST_OPTIONS,
    SKILL_OPTIONS,
    SUBJECT_OPTIONS,
    WORK_STYLE_OPTIONS,
    DEGREE_BRANCH_OPTIONS
)
from recommender import match_careers
from roadmap import analyze_skill_gap, generate_30_day_roadmap
from database import init_db, save_assessment, get_all_assessments, get_assessment_by_id, delete_assessment
from ai_helper import is_ai_available, generate_ai_career_explanation, ask_ai_career_assistant

# Ensure database is initialized
init_db()

# Custom CSS for high accessibility, clean cards, and polished presentation
st.markdown("""
<style>
    /* Main typography & headers */
    .app-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.1rem;
        letter-spacing: -0.5px;
    }
    .app-subtitle {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.2rem;
    }
    .disclaimer-box {
        background-color: #F3F4F6;
        border-left: 4px solid #6B7280;
        padding: 10px 14px;
        border-radius: 4px;
        font-size: 0.88rem;
        color: #374151;
        margin-bottom: 1.2rem;
    }

    /* Cards */
    .career-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: transform 0.15s ease-in-out;
    }
    .career-card:hover {
        border-color: #3B82F6;
        box-shadow: 0 4px 12px rgba(59,130,246,0.1);
    }
    .rank-badge {
        font-size: 0.82rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 9999px;
        display: inline-block;
        margin-bottom: 8px;
    }
    .rank-1 { background-color: #FEF3C7; color: #92400E; border: 1px solid #FCD34D; }
    .rank-2 { background-color: #E0E7FF; color: #3730A3; border: 1px solid #C7D2FE; }
    .rank-3 { background-color: #F3E8FF; color: #6B21A8; border: 1px solid #E9D5FF; }

    /* Match score pill */
    .score-pill {
        font-size: 1.2rem;
        font-weight: 800;
        color: #1D4ED8;
    }

    /* Tags / Chips */
    .skill-chip {
        display: inline-block;
        padding: 4px 10px;
        margin: 3px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .chip-acquired {
        background-color: #D1FAE5;
        color: #065F46;
        border: 1px solid #A7F3D0;
    }
    .chip-missing {
        background-color: #FEE2E2;
        color: #991B1B;
        border: 1px solid #FECACA;
    }
    .chip-info {
        background-color: #EFF6FF;
        color: #1E40AF;
        border: 1px solid #BFDBFE;
    }

    /* Starter project card */
    .project-card {
        background-color: #F8FAFC;
        border: 1px solid #CBD5E1;
        border-radius: 10px;
        padding: 16px;
        margin-top: 12px;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Session State
if "profile" not in st.session_state:
    st.session_state.profile = None
if "recommendations" not in st.session_state:
    st.session_state.recommendations = None
if "ai_explanation" not in st.session_state:
    st.session_state.ai_explanation = None
if "selected_career_tab" not in st.session_state:
    st.session_state.selected_career_tab = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def render_sidebar():
    """Render sidebar navigation and app status."""
    with st.sidebar:
        st.markdown("### 🧭 **Navigation**")
        page = st.radio(
            "Go to",
            [
                "📝 Career Assessment",
                "📂 Saved Assessments",
                "📖 Career Catalogue",
                "💬 AI Career Assistant",
                "ℹ️ Demo Guide & About"
            ],
            index=0
        )

        st.divider()

        # System Status Indicator
        st.markdown("### ⚙️ **System Status**")
        ai_active = is_ai_available()
        if ai_active:
            st.success("🟢 Gemini API: Connected")
        else:
            st.info("🟡 Gemini API: Demo Mode (Offline / Rule-Based)")
            st.caption("Add `GEMINI_API_KEY` to `.env` to enable live generative AI responses.")

        st.divider()
        st.caption("AI-Powered Career Guidance System • Hackathon Edition")

        return page


def load_demo_profile():
    """Pre-fill session state with the recommended hackathon sample student profile."""
    st.session_state["form_name"] = "Alex Morgan"
    st.session_state["form_branch"] = "B.Tech / B.E. - Artificial Intelligence & Machine Learning (AIML)"
    st.session_state["form_semester"] = 5
    st.session_state["form_interests"] = ["Problem Solving", "AI & Machine Learning", "Mathematics & Statistics"]
    st.session_state["form_skills"] = ["Python", "SQL", "Statistics & Probability"]
    st.session_state["form_custom_skills"] = "Git basics, Pandas"
    st.session_state["form_subjects"] = ["Programming & Algorithms", "Statistics & Probability", "Machine Learning"]
    st.session_state["form_work_style"] = "Analytical & Research-Oriented"


def render_assessment_page():
    """Main Assessment Form, Career Recommendations, Skill Gap & 30-Day Roadmap."""
    st.markdown('<div class="app-title">AI-Powered Career Guidance System 🧭</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-subtitle">Discover high-fit career paths, diagnose your skill gaps, '
        'and generate an actionable 30-day learning roadmap tailored to your coursework and interests.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="disclaimer-box">'
        '⚠️ <strong>Exploration Tool Disclaimer:</strong> This system is designed for student exploration, '
        'skill gap discovery, and learning roadmap generation. Scores are calculated transparently using heuristic overlap '
        'and do not represent a guarantee of admission, hiring, salary, or psychometric career destiny.'
        '</div>',
        unsafe_allow_html=True
    )

    # Demo quick-loader bar
    col_demo, col_clear = st.columns([3, 1])
    with col_demo:
        if st.button("⚡ Fill Sample Demo Profile (AIML Student)", help="Click to instantly prefill a realistic profile for live hackathon demonstration"):
            load_demo_profile()
            st.rerun()
    with col_clear:
        if st.button("🔄 Reset Profile"):
            st.session_state.profile = None
            st.session_state.recommendations = None
            st.session_state.ai_explanation = None
            for key in ["form_name", "form_branch", "form_semester", "form_interests", "form_skills", "form_custom_skills", "form_subjects", "form_work_style"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    # Profile Entry Form
    with st.expander("📋 Student Profile & Preferences Form", expanded=(st.session_state.recommendations is None)):
        with st.form("student_profile_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                name = st.text_input(
                    "Name or Nickname (Optional)",
                    value=st.session_state.get("form_name", ""),
                    placeholder="e.g. Alex"
                )
                branch = st.selectbox(
                    "Degree & Branch *",
                    options=DEGREE_BRANCH_OPTIONS,
                    index=DEGREE_BRANCH_OPTIONS.index(st.session_state.get("form_branch", DEGREE_BRANCH_OPTIONS[0]))
                    if st.session_state.get("form_branch") in DEGREE_BRANCH_OPTIONS else 0
                )
                semester = st.slider(
                    "Current Semester *",
                    min_value=1,
                    max_value=8,
                    value=st.session_state.get("form_semester", 4)
                )

            with col_b:
                work_style = st.selectbox(
                    "Preferred Work Style *",
                    options=WORK_STYLE_OPTIONS,
                    index=WORK_STYLE_OPTIONS.index(st.session_state.get("form_work_style", WORK_STYLE_OPTIONS[0]))
                    if st.session_state.get("form_work_style") in WORK_STYLE_OPTIONS else 0,
                    help="How you prefer to spend your day-to-day project time"
                )
                subjects = st.multiselect(
                    "Subjects / Coursework Enjoyed *",
                    options=SUBJECT_OPTIONS,
                    default=st.session_state.get("form_subjects", ["Programming & Algorithms", "Database Systems"])
                )

            st.markdown("#### 🎯 Interests & Current Technical Capabilities")
            interests = st.multiselect(
                "Select Your Key Technical Interests *",
                options=INTEREST_OPTIONS,
                default=st.session_state.get("form_interests", ["Problem Solving", "AI & Machine Learning"])
            )

            col_s1, col_s2 = st.columns(2)
            with col_s1:
                skills = st.multiselect(
                    "Select Your Current Skills *",
                    options=SKILL_OPTIONS,
                    default=st.session_state.get("form_skills", ["Python", "SQL"])
                )
            with col_s2:
                custom_skills_input = st.text_input(
                    "Additional Custom Skills (Comma separated)",
                    value=st.session_state.get("form_custom_skills", ""),
                    placeholder="e.g. Git, Flask, NumPy"
                )

            st.caption("🔒 Privacy Assurance: We do not collect phone numbers, addresses, passwords, or personal identity documents.")

            submitted = st.form_submit_button("🚀 Generate Career Recommendations & Roadmap", type="primary", use_container_width=True)

            if submitted:
                # Parse custom skills
                parsed_custom = [s.strip() for s in custom_skills_input.split(",") if s.strip()]
                all_skills = list(dict.fromkeys(skills + parsed_custom))

                # Validation checks
                validation_errors = []
                if not interests:
                    validation_errors.append("Please select at least one interest to help us identify relevant careers.")
                if not all_skills:
                    validation_errors.append("Please select or enter at least one current skill (even basics like Python, HTML, or SQL).")
                if not subjects:
                    validation_errors.append("Please select at least one subject or coursework area you enjoyed.")

                if validation_errors:
                    for err in validation_errors:
                        st.error(f"⚠️ {err}")
                else:
                    # Build profile dict
                    profile_data = {
                        "name": name.strip(),
                        "degree_branch": branch,
                        "semester": semester,
                        "interests": interests,
                        "skills": all_skills,
                        "subjects_enjoyed": subjects,
                        "work_style": work_style
                    }

                    # Compute transparent match scores
                    with st.spinner("Analyzing profile and matching career pathways..."):
                        matches = match_careers(profile_data, top_n=3)
                        explanation = generate_ai_career_explanation(profile_data, matches)

                    st.session_state.profile = profile_data
                    st.session_state.recommendations = matches
                    st.session_state.ai_explanation = explanation
                    st.session_state.selected_career_tab = matches[0]["title"]
                    st.rerun()

    # Display Results if Available
    if st.session_state.recommendations:
        render_results_section()


def render_results_section():
    """Render top 3 recommendations, skill gap analysis, and 30-day roadmap."""
    profile = st.session_state.profile
    recs = st.session_state.recommendations
    explanation = st.session_state.ai_explanation

    st.markdown("---")
    st.markdown("### 🏆 **Your Top 3 Career Recommendations**")
    st.caption("Calculated using transparent heuristic matching based on your declared interests, skills, coursework, and work style.")

    cols = st.columns(3)
    rank_labels = ["🥇 Primary Match", "🥈 Strong Contender", "🥉 High-Potential Horizon"]
    rank_classes = ["rank-1", "rank-2", "rank-3"]

    for i, col in enumerate(cols):
        with col:
            r = recs[i]
            st.markdown(f"""
            <div class="career-card">
                <span class="rank-badge {rank_classes[i]}">{rank_labels[i]}</span>
                <div style="font-size: 1.3rem; font-weight: 700; color: #111827;">{r['title']}</div>
                <div style="font-size: 0.85rem; color: #6B7280; margin-bottom: 8px;">{r['category']}</div>
                <div class="score-pill">{r['match_score']}% Match</div>
                <p style="font-size: 0.88rem; color: #4B5563; margin-top: 8px; min-height: 55px;">{r['description']}</p>
                <div style="font-size: 0.82rem; color: #374151; font-weight: 600;">Match Factors:</div>
                <ul style="font-size: 0.8rem; color: #4B5563; padding-left: 18px; margin-top: 4px;">
                    {''.join(f'<li>{reason}</li>' for reason in r['reasons'][:2])}
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # Detailed Career Explorer Tabs
    st.markdown("---")
    st.markdown("### 🔍 **Deep Dive: Skill-Gap Analysis & Practical Roadmap**")
    st.caption("Select one of your top careers below to inspect skill gaps and generate a 30-day study plan:")

    career_titles = [r["title"] for r in recs]
    selected_career = st.radio(
        "Select Career Path to Inspect:",
        options=career_titles,
        horizontal=True,
        index=0
    )

    # Retrieve selected career data
    target_career_obj = next(r for r in recs if r["title"] == selected_career)
    gap_data = analyze_skill_gap(profile["skills"], selected_career)
    roadmap_data = generate_30_day_roadmap(profile, selected_career)

    tab_gap, tab_roadmap, tab_ai, tab_save = st.tabs([
        "📊 Skill-Gap Analysis",
        "📅 30-Day Learning Roadmap",
        "💡 AI Career Advice & Insights",
        "💾 Save & Export Results"
    ])

    # Tab 1: Skill Gap Analysis
    with tab_gap:
        col_g1, col_g2 = st.columns([1, 1])

        with col_g1:
            st.markdown("#### 🟢 Skills You Already Have")
            if gap_data["acquired"]:
                st.markdown(
                    "".join(f'<span class="skill-chip chip-acquired">✓ {s}</span>' for s in gap_data["acquired"]),
                    unsafe_allow_html=True
                )
                st.caption(f"You have acquired {len(gap_data['acquired'])} out of {gap_data['total_required']} prerequisite skills.")
            else:
                st.info("You haven't listed any of the core prerequisite skills yet. Starting fresh is completely fine!")

            st.markdown("#### 🔴 Skills to Learn Next (Skill Gap)")
            if gap_data["missing"]:
                st.markdown(
                    "".join(f'<span class="skill-chip chip-missing">⚡ {s}</span>' for s in gap_data["missing"]),
                    unsafe_allow_html=True
                )
                st.caption("Focus your next 30 days on acquiring these missing high-impact competencies.")
            else:
                st.success("🎉 Outstanding! You already possess all primary beginner skills for this path.")

        with col_g2:
            st.markdown("#### 📈 Prerequisite Readiness Level")
            st.metric(
                label=f"Readiness Index for {selected_career}",
                value=f"{gap_data['readiness_pct']}%",
                delta=f"{len(gap_data['acquired'])} / {gap_data['total_required']} skills unlocked"
            )
            st.progress(gap_data["readiness_pct"] / 100.0)

            st.markdown("#### 🎯 Core Learning Topics to Master First")
            for topic in target_career_obj["beginner_learning_topics"][:4]:
                st.markdown(f"- 📘 {topic}")

    # Tab 2: 30-Day Roadmap
    with tab_roadmap:
        st.markdown(f"#### 🚀 30-Day Action Sprint for **{selected_career}**")
        st.caption(roadmap_data["overview"])

        for week in roadmap_data["weeks"]:
            with st.expander(f"📌 {week['title']}", expanded=(week['week_number'] == 1)):
                st.markdown(f"**Goal**: {week['goal']}")
                st.markdown(f"**Weekly Milestone**: `{week['milestone']}`")
                st.markdown("**Actionable Tasks**:")
                for task in week["tasks"]:
                    st.markdown(f"- [ ] {task}")

        # Starter Portfolio Project Card
        proj = roadmap_data["starter_project"]
        st.markdown(f"""
        <div class="project-card">
            <div style="font-size: 1.15rem; font-weight: 700; color: #1E3A8A;">📦 Starter Portfolio Project: {proj['title']}</div>
            <div style="font-size: 0.88rem; color: #4B5563; margin-top: 4px;"><strong>Objective:</strong> {proj['objective']}</div>
            <div style="font-size: 0.85rem; color: #1E40AF; margin-top: 6px;"><strong>Tech Stack:</strong> <code>{proj['tech_stack']}</code></div>
        </div>
        """, unsafe_allow_html=True)

    # Tab 3: AI Career Advice
    with tab_ai:
        st.markdown("#### 💡 AI-Generated Career Evaluation & Strategy")
        if explanation:
            if explanation["source"] == "gemini_ai":
                st.success("✨ Powered by Google Gemini API (Live Generation)")
            else:
                st.info("⚡ Hackathon Demo Mode (Structured Rule-Based Insight)")

            st.markdown(explanation["text"])
        else:
            st.info("Click 'Generate Career Recommendations' above to produce AI analysis.")

    # Tab 4: Save & Export
    with tab_save:
        st.markdown("#### 💾 Save to Assessment History")
        st.write("Save your profile and recommendations locally in SQLite so you can review them at any time.")

        if st.button("💾 Save Assessment to Database", type="primary"):
            row_id = save_assessment(profile, recs)
            if row_id > 0:
                st.success(f"✅ Assessment successfully saved to SQLite database with Record ID #{row_id}!")
            else:
                st.error("Failed to save assessment to database. Please check permissions.")

        st.markdown("---")
        st.markdown("#### 📥 Export Learning Roadmap as Markdown")
        export_text = f"""# Career Guidance & 30-Day Learning Plan
**Student**: {profile.get('name') or 'Student'}
**Degree / Branch**: {profile.get('degree_branch')} (Semester {profile.get('semester')})
**Target Career**: {selected_career} (Match Score: {target_career_obj['match_score']}%)

---

## 1. Skill Gap Summary
- **Skills Already Acquired**: {', '.join(gap_data['acquired']) if gap_data['acquired'] else 'None yet'}
- **Skills to Learn Next**: {', '.join(gap_data['missing'])}
- **Initial Readiness**: {gap_data['readiness_pct']}%

---

## 2. 30-Day (4-Week) Action Roadmap
"""
        for w in roadmap_data["weeks"]:
            export_text += f"\n### {w['title']}\n"
            export_text += f"- **Goal**: {w['goal']}\n"
            export_text += f"- **Milestone**: {w['milestone']}\n"
            for t in w["tasks"]:
                export_text += f"- [ ] {t}\n"

        export_text += f"""
---

## 3. Starter Portfolio Project
- **Project Title**: {proj['title']}
- **Tech Stack**: {proj['tech_stack']}
- **Objective**: {proj['objective']}

*Generated by AI-Powered Career Guidance System (Google Antigravity Hackathon Edition)*
"""
        st.download_button(
            label="📄 Download 30-Day Roadmap (.md)",
            data=export_text,
            file_name=f"career_roadmap_{selected_career.replace(' ', '_').lower()}.md",
            mime="text/markdown"
        )


def render_saved_assessments_page():
    """View and manage saved assessments from SQLite."""
    st.markdown('<div class="app-title">📂 Saved Assessments History</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Review previously generated recommendations and learning plans.</div>', unsafe_allow_html=True)

    records = get_all_assessments()

    if not records:
        st.info("No saved assessments found in the database. Complete the assessment form and click 'Save Assessment' to store records here.")
        return

    st.write(f"Total Saved Records: **{len(records)}**")

    for rec in records:
        with st.expander(f"👤 #{rec['id']} - {rec['student_name']} ({rec['degree_branch']}) | Top Match: {rec['top_career']} ({rec['top_match_score']}%)"):
            col_info, col_actions = st.columns([3, 1])

            with col_info:
                st.write(f"**Recorded Date**: {rec['created_at']}")
                st.write(f"**Semester**: {rec['semester']}")
                st.write(f"**Top Career**: `{rec['top_career']}` ({rec['top_match_score']}%)")

                # Fetch full details
                full_rec = get_assessment_by_id(rec["id"])
                if full_rec:
                    st.write(f"**Interests**: {', '.join(full_rec.get('interests', []))}")
                    st.write(f"**Skills**: {', '.join(full_rec.get('skills', []))}")
                    st.write(f"**Work Style**: {full_rec.get('work_style')}")

            with col_actions:
                if st.button("🗑️ Delete", key=f"del_{rec['id']}"):
                    if delete_assessment(rec["id"]):
                        st.success("Deleted!")
                        st.rerun()

                if st.button("🔄 Reload into Dashboard", key=f"reload_{rec['id']}"):
                    full_rec = get_assessment_by_id(rec["id"])
                    st.session_state.profile = {
                        "name": full_rec.get("student_name"),
                        "degree_branch": full_rec.get("degree_branch"),
                        "semester": full_rec.get("semester"),
                        "interests": full_rec.get("interests", []),
                        "skills": full_rec.get("skills", []),
                        "subjects_enjoyed": full_rec.get("subjects_enjoyed", []),
                        "work_style": full_rec.get("work_style")
                    }
                    st.session_state.recommendations = full_rec.get("recommendations_json", [])
                    st.session_state.ai_explanation = generate_ai_career_explanation(
                        st.session_state.profile, st.session_state.recommendations
                    )
                    st.success("Assessment reloaded! Return to 'Career Assessment' in the sidebar.")


def render_career_catalogue_page():
    """Browse all 8 careers in the catalogue."""
    st.markdown('<div class="app-title">📖 Career Catalogue Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Browse all 8 technology pathways, prerequisites, and starter projects.</div>', unsafe_allow_html=True)

    for title, career in CAREER_CATALOGUE.items():
        with st.expander(f"💼 {title} ({career['category']})"):
            st.write(career["description"])

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Key Required Skills:**")
                for s in career["required_skills"]:
                    st.markdown(f"- `{s}`")
            with col2:
                st.markdown("**Relevant Interests:**")
                for i in career["relevant_interests"]:
                    st.markdown(f"- {i}")

            st.markdown(f"**Starter Project**: *{career['starter_project']['title']}*")
            st.caption(career['starter_project']['objective'])


def render_ai_assistant_page():
    """Interactive follow-up Q&A assistant grounded in the student's submitted profile."""
    st.markdown('<div class="app-title">💬 AI Career Assistant</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-subtitle">Ask questions about preparation strategies, resumes, interviews, or study time balance.</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.recommendations:
        st.warning("⚠️ Please complete the **Career Assessment** first so the AI assistant can provide personalized guidance.")
        return

    profile = st.session_state.profile
    top_career = st.session_state.recommendations[0]["title"]

    st.info(f"Targeting: **{top_career}** for **{profile.get('name') or 'Student'}** ({profile.get('degree_branch')})")

    # Quick prompt buttons
    st.markdown("##### Quick Questions:")
    q_cols = st.columns(3)
    preset_q = None
    if q_cols[0].button("📄 How should I format my resume?"):
        preset_q = "How should I format my resume for this career path?"
    if q_cols[1].button("⏱️ How can I balance 5 hours a week?"):
        preset_q = "How can I balance 5 hours a week of study alongside college coursework?"
    if q_cols[2].button("💼 What are common interview topics?"):
        preset_q = "What are the most common interview topics for beginner roles in this field?"

    user_query = st.chat_input("Ask a follow-up question about your career roadmap...")
    effective_query = preset_q or user_query

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if effective_query:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": effective_query})
        with st.chat_message("user"):
            st.markdown(effective_query)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Consulting career assistant..."):
                response_text = ask_ai_career_assistant(profile, top_career, effective_query)
            st.markdown(response_text)

        st.session_state.chat_history.append({"role": "assistant", "content": response_text})


def render_demo_guide_page():
    """Hackathon demo guide, presentation walkthrough, and methodology."""
    st.markdown('<div class="app-title">ℹ️ Hackathon Demo Guide & System Architecture</div>', unsafe_allow_html=True)

    st.markdown("""
### 🎯 **Hackathon Presentation Pitch (2-Minute Blueprint)**
1. **The Problem (20 sec)**: Engineering and computer science students often face choice overload: they aren't sure which tech career path matches their actual interests, and they lack a structured, realistic roadmap to bridge skill deficits.
2. **The Solution (30 sec)**: **AI-Powered Career Guidance System** collects high-level student profile preferences without asking for sensitive PII, calculates a transparent match score against 8 industry career paths, isolates the missing skills, and constructs a 30-day (4-week) actionable study sprint with a concrete starter project.
3. **Live Demonstration (40 sec)**:
   - Click **'Fill Sample Demo Profile'** on the assessment page.
   - Show how the transparent matching engine scores **Data Scientist** and **ML Engineer** near the top.
   - Point out the **Skill-Gap Analysis** showing what the student already has vs. what to learn next.
   - Expand the **4-Week Roadmap** to show weekly milestones and the starter portfolio project.
4. **AI Layer & Resiliency (20 sec)**: Powered by the Google Gen AI SDK (Gemini), with deterministic Demo Mode fallback ensuring zero failures even if Wi-Fi drops.
5. **Close & Ethics (10 sec)**: Highlight our responsible AI disclaimer: this tool empowers student exploration and does not replace human counselors.

---

### 🏗️ **System Architecture & Design Decisions**
- **Streamlit**: Single-page reactive Python interface without separate frontend dependencies.
- **Transparent Matching Engine**: Heuristic scoring based on weighted multi-set overlap (Interests 40%, Skills 35%, Coursework 15%, Work Style 10%).
- **SQLite Database**: Local lightweight persistence with parameterized queries for saving and reviewing assessments.
- **Google Gen AI (Gemini)**: Produces natural language career syntheses and powers an interactive Q&A assistant.
""")


def main():
    page = render_sidebar()

    if page == "📝 Career Assessment":
        render_assessment_page()
    elif page == "📂 Saved Assessments":
        render_saved_assessments_page()
    elif page == "📖 Career Catalogue":
        render_career_catalogue_page()
    elif page == "💬 AI Career Assistant":
        render_ai_assistant_page()
    elif page == "ℹ️ Demo Guide & About":
        render_demo_guide_page()


if __name__ == "__main__":
    main()
