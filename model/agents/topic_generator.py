from utils.shivaay_api import call_shivaay_agent
import json

def generate_topics_from_portfolio(portfolio_json):
    """
    Uses Shivaay model to recommend 3–4 trending course topics based on the user's skillset.
    """
    system_prompt = (
        "You are an expert AI career analyst that suggests trending learning domains "
        "and emerging technologies for upskilling. Output must be a JSON list."
    )

    user_prompt = f"""
    User has the following skillset:
    {', '.join(portfolio_json.get('highlighted_skills', []))}

    Based on their skills, suggest 3 to 4 trending topics, domains, or technologies
    they should explore for online courses and upskilling.
    Example output:
    ["AI Agents", "Web3 Development", "Data Engineering", "Cloud DevOps"]
    """

    try:
        response = call_shivaay_agent(system_prompt, user_prompt)
        topics = json.loads(response)
    except Exception:
        # fallback if model returns text instead of JSON
        topics = [line.strip("-• ").strip() for line in response.split("\n") if line.strip()]

    return topics[:4] 