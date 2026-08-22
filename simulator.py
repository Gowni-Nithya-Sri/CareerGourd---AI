from data.careers import CAREERS
from core.readiness import calculate_readiness
import json


# ===================================================
# 1. Load learning data
# ===================================================

def load_learning_data():

    with open(
        "data/learning_data.json",
        "r"
    ) as file:

        return json.load(file)


# ===================================================
# 2. Get skill importance for target job
# ===================================================

def get_skill_weights(target_job):

    job = CAREERS[target_job]

    skill_weights = {}

    for category, skills in job.items():

        for skill, weight in skills.items():

            skill_weights[skill] = weight

    return skill_weights


# ===================================================
# 3. Allocate study time among missing skills
# ===================================================

def allocate_study_time(
    missing_skills,
    study_hours_per_day,
    days
):

    learning_data = load_learning_data()

    total_available_hours = (
        study_hours_per_day * days
    )

    skill_scores = {}

    # -----------------------------------------------
    # Calculate priority for each missing skill
    # -----------------------------------------------

    for item in missing_skills:

        skill = item["skill"]

        importance = item["weight"]

        # Skill not present in learning database
        if skill not in learning_data:
            continue

        required_hours = learning_data[
            skill
        ]["hours"]

        # Higher importance + lower learning time
        # = higher priority
        priority = (
            importance ** 1.5
        ) / required_hours

        skill_scores[skill] = priority

    # -----------------------------------------------
    # No skills available for learning
    # -----------------------------------------------

    if not skill_scores:
        return {}

    total_priority = sum(
        skill_scores.values()
    )

    allocated_hours = {}

    # -----------------------------------------------
    # Distribute study time
    # -----------------------------------------------

    for skill, priority in skill_scores.items():

        hours = (
            priority / total_priority
        ) * total_available_hours

        allocated_hours[skill] = round(
            hours,
            2
        )

    return allocated_hours


# ===================================================
# 4. Calculate future skill levels
# ===================================================

def simulate_future_skills(
    current_skill_levels,
    allocated_hours
):

    learning_data = load_learning_data()

    future_levels = (
        current_skill_levels.copy()
    )

    for skill, hours in allocated_hours.items():

        if skill not in learning_data:
            continue

        required_hours = learning_data[
            skill
        ]["hours"]

        efficiency = learning_data[
            skill
        ]["efficiency"]

        current_level = future_levels.get(
            skill,
            0
        )

        # -------------------------------------------
        # Calculate raw learning progress
        # -------------------------------------------

        raw_progress = (
            hours / required_hours
        ) * 100

        raw_progress *= efficiency

        # -------------------------------------------
        # Diminishing returns
        # -------------------------------------------

        if current_level < 40:

            progress_multiplier = 1.0

        elif current_level < 70:

            progress_multiplier = 0.75

        elif current_level < 90:

            progress_multiplier = 0.50

        else:

            progress_multiplier = 0.25

        improvement = (
            raw_progress
            * progress_multiplier
        )

        future_level = (
            current_level + improvement
        )

        # -------------------------------------------
        # Never exceed 100%
        # -------------------------------------------

        future_level = min(
            future_level,
            100
        )

        future_levels[skill] = round(
            future_level,
            2
        )

    return future_levels


# ===================================================
# 5. Run complete career simulation
# ===================================================

def run_career_simulation(
    current_skill_levels,
    target_job,
    study_hours_per_day,
    days_list
):

    results = []

    # -----------------------------------------------
    # Get target career skill weights
    # -----------------------------------------------

    skill_weights = get_skill_weights(
        target_job
    )

    # -----------------------------------------------
    # Simulate each time period
    # -----------------------------------------------

    for days in days_list:

        # -------------------------------------------
        # Total study time
        # -------------------------------------------

        total_hours = (
            study_hours_per_day * days
        )

        # -------------------------------------------
        # Find skills that need improvement
        # -------------------------------------------

        missing_skills = []

        for skill, weight in skill_weights.items():

            current_level = (
                current_skill_levels.get(
                    skill,
                    0
                )
            )

            if current_level < 100:

                missing_skills.append({

                    "skill": skill,

                    "weight": weight

                })

        # -------------------------------------------
        # Allocate study hours
        # -------------------------------------------

        allocated_hours = allocate_study_time(

            missing_skills,

            study_hours_per_day,

            days

        )

        # -------------------------------------------
        # Calculate future skill levels
        # -------------------------------------------

        future_skills = simulate_future_skills(

            current_skill_levels,

            allocated_hours

        )

        # -------------------------------------------
        # Calculate future readiness
        # -------------------------------------------

        future_readiness = calculate_readiness(

            future_skills,

            target_job

        )

        # -------------------------------------------
        # Store result
        # -------------------------------------------

        results.append({

            "days": days,

            "study_hours": total_hours,

            "skills": future_skills,

            "allocated_hours": allocated_hours,

            "readiness": future_readiness

        })

    return results