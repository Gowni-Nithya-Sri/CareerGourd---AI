from data.careers import CAREERS


CATEGORY_MULTIPLIERS = {
    "essential": 3,
    "important": 2,
    "useful": 1
}


def calculate_readiness(
    user_skill_levels,
    target_job
):

    job = CAREERS[target_job]

    total_weight = 0
    earned_weight = 0

    for category, skills in job.items():

        multiplier = CATEGORY_MULTIPLIERS[category]

        for skill, importance in skills.items():

            adjusted_weight = (
                importance * multiplier
            )

            total_weight += adjusted_weight

            user_level = user_skill_levels.get(
                skill,
                0
            )

            earned_weight += (
                adjusted_weight
                * user_level
                / 100
            )

    if total_weight == 0:
        return 0

    readiness = (
        earned_weight
        / total_weight
    ) * 100

    return round(readiness, 2)