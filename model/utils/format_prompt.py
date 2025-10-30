def portfolio_to_prompt(portfolio_json: dict) -> str:
    skills = ", ".join(portfolio_json.get("skills", []))
    education = portfolio_json.get("education", "Not provided")
    experience = ", ".join(portfolio_json.get("experience", []))
    projects = ", ".join(portfolio_json.get("projects", [])) if "projects" in portfolio_json else "None"

    return (
        f"The user has the following skills: {skills}.\n"
        f"Education background: {education}.\n"
        f"Experience includes: {experience}.\n"
        f"Projects worked on: {projects}.\n"
        f"Based on this portfolio, recommend suitable career paths, possible industries, and skill improvement suggestions."
    )

