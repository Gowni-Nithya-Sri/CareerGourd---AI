from data.careers import CAREERS


def analyze_skill_gap(
    user_skills,
    target_job
):

    job = CAREERS[target_job]

    all_skills = {}

    # Combine all categories
    for category, skills in job.items():

        for skill, weight in skills.items():

            all_skills[skill] = weight

    user_skills = set(user_skills)

    have = []
    missing = []

    for skill, weight in all_skills.items():

        if skill in user_skills:

            have.append(skill)

        else:

            missing.append({
                "skill": skill,
                "weight": weight
            })

    # Sort by importance
    missing.sort(
        key=lambda x: x["weight"],
        reverse=True
    )

    return have, missing