import streamlit as st
import pandas as pd

from core.readiness import calculate_readiness
from core.skill_gap import analyze_skill_gap
from core.simulator import run_career_simulation
from core.resume_parser import (
    extract_resume_text,
    detect_skills
)
from core.roadmap import (
    create_learning_roadmap,
    create_daily_mission
)

from data.careers import CAREERS


# =========================================
# PAGE CONFIGURATION
# =========================================

st.set_page_config(
    page_title="CareerGourd AI",
    page_icon="🥕",
    layout="wide"
)


# =========================================
# TITLE
# =========================================

st.title("🥕 CareerGourd AI")

st.subheader("Your Career GPS")

st.write(
    "Discover your career readiness, identify skill gaps, "
    "simulate your future career growth, and get a "
    "personalized learning roadmap."
)


# =========================================
# INITIALIZE VARIABLES
# =========================================

detected_skills = []
skill_levels = {}
resume_text = ""


# =========================================
# RESUME UPLOAD
# =========================================

st.header("📄 Upload Your Resume")

st.write(
    "Upload your resume and CareerGourd will analyze "
    "your skills and career readiness."
)

uploaded_resume = st.file_uploader(
    "Choose your resume",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=False
)


# =========================================
# PROCESS RESUME
# =========================================

if uploaded_resume is not None:

    st.success(
        f"Resume uploaded successfully: "
        f"{uploaded_resume.name}"
    )

    st.write(
        "File size:",
        round(
            uploaded_resume.size / 1024,
            2
        ),
        "KB"
    )

    # -----------------------------------------
    # Extract resume text
    # -----------------------------------------

    resume_text = extract_resume_text(
        uploaded_resume
    )

    if resume_text and resume_text.strip():

        st.success(
            "✅ Resume text extracted successfully!"
        )

        # -----------------------------------------
        # Detect skills
        # -----------------------------------------

        detected_skills = detect_skills(
            resume_text
        )

        # Remove duplicate skills
        detected_skills = list(
            dict.fromkeys(
                detected_skills
            )
        )

        st.subheader(
            "🧠 Skills Detected From Your Resume"
        )

        if detected_skills:

            st.write(
                "CareerGourd found these skills:"
            )

            for skill in detected_skills:

                st.write(
                    f"✅ {skill}"
                )

        else:

            st.warning(
                "No recognized skills were found "
                "in your resume."
            )

    else:

        st.error(
            "❌ Could not extract text from "
            "this resume."
        )


# =========================================
# USER INFORMATION
# =========================================

st.header("👤 Tell Us About Yourself")


# =========================================
# TARGET JOB
# =========================================

target_job = st.selectbox(
    "🎯 What job are you targeting?",
    list(CAREERS.keys())
)


# =========================================
# STUDY HOURS
# =========================================

st.subheader("⏱️ What-If Career Simulator")

st.write(
    "What happens to your career readiness "
    "if you change your daily study time?"
)

study_hours = st.slider(
    "📚 Study hours per day",
    min_value=1,
    max_value=8,
    value=2,
    step=1
)

st.info(
    f"You're planning to study "
    f"**{study_hours} hours/day**."
)


# =========================================
# RESUME SKILL PROFICIENCY
# =========================================

if uploaded_resume is not None and detected_skills:

    st.header("🧠 Skills Found in Your Resume")

    st.write(
        "CareerGourd automatically detected these "
        "skills from your resume:"
    )

    for skill in detected_skills:

        st.write(
            f"✅ {skill}"
        )

    # -----------------------------------------
    # Skill proficiency
    # -----------------------------------------

    st.subheader(
        "📊 Rate Your Proficiency"
    )

    st.caption(
        "Rate your current level for each detected "
        "skill so CareerGourd can calculate your readiness."
    )

    for index, skill in enumerate(
        detected_skills
    ):

        level = st.slider(
            f"{skill}",
            min_value=0,
            max_value=100,
            value=50,
            step=5,

            # IMPORTANT:
            # index makes every widget unique
            key=f"resume_skill_{index}_{skill}"
        )

        skill_levels[skill] = level


# =========================================
# ANALYZE BUTTON
# =========================================

if st.button(
    "🚀 Analyze My Career",
    use_container_width=True
):

    # =====================================
    # VALIDATION
    # =====================================

    if uploaded_resume is None:

        st.warning(
            "📄 Please upload your resume first."
        )

        st.stop()


    if not detected_skills:

        st.warning(
            "⚠️ No recognized skills were detected "
            "from your resume."
        )

        st.stop()


    # =====================================
    # CALCULATE READINESS
    # =====================================

    readiness = calculate_readiness(
        skill_levels,
        target_job
    )


    # =====================================
    # ANALYZE SKILL GAPS
    # =====================================

    skills_have, skills_missing = (
        analyze_skill_gap(
            detected_skills,
            target_job
        )
    )


    # =====================================
    # CAREER DIGITAL TWIN
    # =====================================

    st.divider()

    st.header(
        "🎯 Your Career Digital Twin"
    )

    col1, col2, col3 = st.columns(3)


    # -------------------------------------
    # Readiness
    # -------------------------------------

    with col1:

        st.metric(
            "Career Readiness",
            f"{readiness}%"
        )


    # -------------------------------------
    # Target Career
    # -------------------------------------

    with col2:

        st.metric(
            "Target Career",
            target_job
        )


    # -------------------------------------
    # Study Time
    # -------------------------------------

    with col3:

        st.metric(
            "Study Time",
            f"{study_hours} hrs/day"
        )


    # =====================================
    # SKILL STRENGTHS
    # =====================================

    st.subheader(
        "✅ Skills You Have"
    )

    if skills_have:

        for skill in skills_have:

            level = skill_levels.get(
                skill,
                0
            )

            st.write(
                f"✓ {skill} — {level}%"
            )

    else:

        st.write(
            "No matching target-job skills yet."
        )


    # =====================================
    # SKILL GAPS
    # =====================================

    st.subheader(
        "⚠️ Skills You Need"
    )

    if skills_missing:

        for item in skills_missing:

            st.write(
                f"🔴 {item['skill']} "
                f"— importance "
                f"{item['weight']}/10"
            )

    else:

        st.success(
            "🎉 You currently have all "
            "required skills!"
        )


    # =====================================
    # CAREER SIMULATION
    # =====================================

    st.divider()

    st.header(
        "📈 Career Forecast"
    )

    simulation_days = [
        30,
        60,
        90
    ]

    results = run_career_simulation(
        skill_levels,
        target_job,
        study_hours,
        simulation_days
    )


    # =====================================
    # FORECAST CARDS
    # =====================================

    forecast_cols = st.columns(3)

    for index, result in enumerate(
        results
    ):

        with forecast_cols[index]:

            st.metric(
                f"📅 {result['days']} Days",
                f"{result['readiness']}%"
            )


    # =====================================
    # READINESS GROWTH CHART
    # =====================================

    st.subheader(
        "📊 Readiness Growth"
    )

    chart_data = pd.DataFrame({

        "Days": [
            0,
            30,
            60,
            90
        ],

        "Readiness": [

            readiness,

            results[0]["readiness"],

            results[1]["readiness"],

            results[2]["readiness"]
        ]
    })

    st.line_chart(
        chart_data,
        x="Days",
        y="Readiness"
    )


    # =====================================
    # PROJECTED SKILL GROWTH
    # =====================================

    st.subheader(
        "🔮 Projected Skill Growth"
    )

    for result in results:

        with st.expander(
            f"{result['days']} Day Projection"
        ):

            st.write(
                "Total study time:",
                result["study_hours"],
                "hours"
            )

            # ---------------------------------
            # Allocated learning time
            # ---------------------------------

            if result.get(
                "allocated_hours"
            ):

                st.write(
                    "📚 Study time allocation:"
                )

                for skill, hours in (
                    result[
                        "allocated_hours"
                    ].items()
                ):

                    st.write(
                        f"• {skill}: "
                        f"{hours} hours"
                    )

            # ---------------------------------
            # Future skill levels
            # ---------------------------------

            for skill, level in (
                result["skills"].items()
            ):

                st.progress(
                    min(
                        level / 100,
                        1.0
                    )
                )

                st.write(
                    f"{skill}: {level}%"
                )


    # =====================================
    # PERSONALIZED LEARNING ROADMAP
    # =====================================

    st.divider()

    st.header(
        "🗺️ Your Personalized Learning Roadmap"
    )

    st.write(
        "CareerGourd has prioritized the skills "
        "you should focus on for your target career."
    )


    roadmap = create_learning_roadmap(
        skill_levels,
        target_job,
        study_hours
    )


    if roadmap:

        for item in roadmap:

            with st.expander(
                f"{item['order']}. "
                f"{item['skill']} "
                f"— {item['current_level']}%"
            ):

                st.write(
                    f"🎯 Importance: "
                    f"{item['importance']}/10"
                )

                st.write(
                    f"📚 Category: "
                    f"{item['category'].title()}"
                )

                st.write(
                    f"⏱️ Estimated learning time: "
                    f"{item['estimated_hours']} hours"
                )

                st.progress(
                    min(
                        item["current_level"] / 100,
                        1.0
                    )
                )

    else:

        st.success(
            "🎉 You have strong proficiency "
            "across the required skills!"
        )


    # =====================================
    # TODAY'S CAREER MISSION
    # =====================================

    st.divider()

    st.header(
        "🎯 Today's Career Mission"
    )


    mission = create_daily_mission(
        roadmap,
        study_hours
    )


    st.info(
        mission["message"]
    )


    if roadmap:

        mission_col1, mission_col2 = (
            st.columns(2)
        )


        with mission_col1:

            st.metric(
                "📖 Learning",
                f"{mission['learning_minutes']} min"
            )


        with mission_col2:

            st.metric(
                "💻 Practice",
                f"{mission['practice_minutes']} min"
            )


        st.write(
            f"**Today's skill:** "
            f"{mission['skill']}"
        )


        st.progress(
            min(
                mission["current_level"] / 100,
                1.0
            )
        )


        st.write(
            f"Current proficiency: "
            f"{mission['current_level']}%"
        )


        st.write(
            "💡 Suggested routine:"
        )

        st.write(
            f"1. 📖 Spend "
            f"{mission['learning_minutes']} minutes "
            f"learning {mission['skill']}."
        )

        st.write(
            f"2. 💻 Spend "
            f"{mission['practice_minutes']} minutes "
            f"practicing {mission['skill']}."
        )

        st.write(
            "3. 📝 Build or solve something small "
            "using what you learned."
        )


    # =====================================
    # FINAL CAREER MESSAGE
    # =====================================

    st.divider()

    st.subheader(
        "🏁 CareerGourd Recommendation"
    )


    if readiness >= 80:

        st.success(
            "🟢 You are approaching "
            "application readiness!"
        )

    elif readiness >= 60:

        st.info(
            "🟡 You have a solid foundation, "
            "but should close your remaining "
            "skill gaps before applying."
        )

    else:

        st.warning(
            "🔴 Focus on your highest-priority "
            "skill gaps before applying."
        )
    # =========================================
# JOB APPLICATION LINKS
# =========================================

st.divider()

st.header("🚀 Start Your Job Search")

st.write(
    f"Ready to explore opportunities for "
    f"**{target_job}**? Use these platforms to "
    f"find relevant jobs."
)

# -----------------------------------------
# Job search URLs
# -----------------------------------------

job_search_urls = {

    "LinkedIn": (
        "https://www.linkedin.com/jobs/search/"
        "?keywords="
    ),

    "Indeed": (
        "https://www.indeed.com/jobs?q="
    ),

    "Glassdoor": (
        "https://www.glassdoor.co.in/Job/"
    )
}

# -----------------------------------------
# Create search query
# -----------------------------------------

search_query = target_job.replace(
    " ",
    "+"
)

# -----------------------------------------
# Display buttons
# -----------------------------------------

col1, col2, col3 = st.columns(3)


with col1:

    st.link_button(
        "💼 Search on LinkedIn",
        job_search_urls["LinkedIn"]
        + search_query,
        use_container_width=True
    )


with col2:

    st.link_button(
        "🔎 Search on Indeed",
        job_search_urls["Indeed"]
        + search_query,
        use_container_width=True
    )


with col3:

    st.link_button(
        "🏢 Search on Glassdoor",
        job_search_urls["Glassdoor"],
        use_container_width=True
    )

    # =====================================
    # FINAL SUMMARY
    # =====================================

    st.success(
        "🥕 CareerGourd has created your "
        "personalized career plan!"
    )