def create_skill_profile(skills):
    """
    Create a dictionary containing
    the user's current skill levels.
    """

    skill_profile = {}

    for skill, level in skills.items():

        level = max(0, min(level, 100))

        skill_profile[skill] = level

    return skill_profile