def is_profile_complete(portfolio_json: dict) -> bool:
    """
    Check if user profile has enough details to generate recommendations.
    Criteria:
    - At least 4 highlighted skills
    - At least 1 previous experience OR education info
    - Optional: some projects, LinkedIn, or contact info
    """
    if not isinstance(portfolio_json, dict):
        return False

    skills = portfolio_json.get("highlighted_skills", [])
    experiences = portfolio_json.get("previous_work_experiences", [])
    education = portfolio_json.get("education", "")
    projects = portfolio_json.get("projects_worked_on", [])

    # Example rule set
    return (
        len(skills) >= 1
        and (len(experiences) >= 0 or bool(education))
        and (len(projects) >= 0 or bool(education))
    )
