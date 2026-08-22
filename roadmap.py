from data.careers import CAREERS
import json


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
# CREATE PERSONALIZED ROADMAP
# =========================================

def create_learning_roadmap(
    skill_levels,
    target_job,
    study_hours
):

    job = CAREERS[target_job]

    learning_data = load_learning_data()

    roadmap = []

    # -----------------------------------------
    # Collect skills required for target job
    # -----------------------------------------

    for category in [
        "essential",
        "important",
        "useful"
    ]:

        for skill, importance in job[
            category
        ].items():

            current_level = skill_levels.get(
                skill,
                0
            )

            # Recommend skills below 80%

            if current_level < 80:

                if skill in learning_data:

                    estimated_hours = (
                        learning_data[skill]["hours"]
                    )

                else:

                    estimated_hours = 20

                roadmap.append({

                    "skill": skill,

                    "category": category,

                    "importance": importance,

                    "current_level": current_level,

                    "estimated_hours":
                        estimated_hours

                })

    # -----------------------------------------
    # Sort by importance
    # -----------------------------------------

    roadmap.sort(
        key=lambda x: (
            x["importance"],
            -x["current_level"]
        ),
        reverse=True
    )

    # -----------------------------------------
    # Add roadmap order
    # -----------------------------------------

    for index, item in enumerate(roadmap):

        item["order"] = index + 1

    return roadmap


# =========================================
# CREATE TODAY'S MISSION
# =========================================

def create_daily_mission(
    roadmap,
    study_hours
):

    # -----------------------------------------
    # No remaining skills
    # -----------------------------------------

    if not roadmap:

        return {

            "skill": "All skills",

            "current_level": 100,

            "learning_minutes": 0,

            "practice_minutes": 0,

            "message": (
                "🎉 Excellent! You have strong "
                "proficiency in the required skills."
            )
        }

    # -----------------------------------------
    # Select highest priority skill
    # -----------------------------------------

    first_skill = roadmap[0]

    total_minutes = study_hours * 60

    learning_minutes = int(
        total_minutes * 0.6
    )

    practice_minutes = int(
        total_minutes * 0.4
    )

    return {

        "skill": first_skill["skill"],

        "current_level":
            first_skill["current_level"],

        "learning_minutes":
            learning_minutes,

        "practice_minutes":
            practice_minutes,

        "message": (
            f"🎯 Today's focus: "
            f"{first_skill['skill']}"
        )
    }