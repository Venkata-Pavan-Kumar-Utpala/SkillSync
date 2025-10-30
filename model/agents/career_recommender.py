from utils.shivaay_api import call_shivaay_agent
from utils.format_prompt import portfolio_to_prompt


def recommend_career(portfolio_json):
    system_prompt = (
        "You are a professional AI career advisor. "
        "Given a candidate's background, analyze their portfolio "
        "and recommend suitable career paths, industries, and next steps."
    )

    # If we received JSON, convert it into a descriptive string
    if isinstance(portfolio_json, dict):
        user_prompt = portfolio_to_prompt(portfolio_json)
    else:
        user_prompt = str(portfolio_json)

    return call_shivaay_agent(system_prompt, user_prompt)
