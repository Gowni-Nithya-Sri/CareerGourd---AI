import json

from data.careers import CAREERS
from core.readiness import calculate_readiness


# =========================================
# BEST CAREER MATCH
# =========================================

def get_career_matches(user_skill_levels):

    results = []

    for career in CAREERS.keys():

        readiness = calculate_readiness(
            user_skill_levels,
            career
        )

        results.append({
            "career": career,
            "readiness": readiness
        })

    # Highest readiness first
    results.sort(
        key=lambda x: x["readiness"],
        reverse=True
    )

    return results


def get_top_career_matches(
    user_skill_levels,
    top_n=3
):

    results = get_career_matches(
        user_skill_levels
    )

    return results[:top_n]


# =========================================
# LOAD LEARNING DATA
# =========================================

def load_learning_data():

    with open(
        "data/learning_data.json",
        "r"
    ) as file:

        return json.load(file)


# =========================================
# PERSONALIZED LEARNING ROADMAP
# =========================================

def create_learning_roadmap(
    user_skill_levels,
    target_job
):

    job = CAREERS[target_job]

    learning_data = load_learning_data()

    roadmap = []

    # -----------------------------------------
    # Combine all career skills
    # -----------------------------------------

    all_skills = {}

    for category, skills in job.items():

        for skill, importance in skills.items():

            all_skills[skill] = {
                "importance": importance,
                "category": category
            }


    # -----------------------------------------
    # Find skill gaps
    # -----------------------------------------

    for skill, info in all_skills.items():

        current_level = user_skill_levels.get(
            skill,
            0
        )

        # Already mastered
        if current_level >= 100:
            continue

        # Learning hours
        if skill in learning_data:

            learning_hours = learning_data[
                skill
            ]["hours"]

        else:

            learning_hours = 0


        # -------------------------------------
        # Calculate remaining learning
        # -------------------------------------

        remaining_percentage = (
            100 - current_level
        )

        estimated_hours = (
            learning_hours
            * remaining_percentage
            / 100
        )


        roadmap.append({

            "skill": skill,

            "current_level": current_level,

            "importance": info["importance"],

            "category": info["category"],

            "estimated_hours": round(
                estimated_hours,
                1
            )

        })


    # -----------------------------------------
    # Sort by importance
    # -----------------------------------------

    roadmap.sort(
        key=lambda x: (
            x["importance"],
            x["current_level"]
        ),
        reverse=True
    )

    return roadmap