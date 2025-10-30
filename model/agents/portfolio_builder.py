from utils.shivaay_api import call_shivaay_agent

def build_portfolio_from_conversation(conversation_history: list):
    """
    Uses Shivaay to analyze conversation and generate portfolio_json.
    """
    text = "\n".join(conversation_history)

    system_prompt = (
        "You are a career data extractor. "
        "Given a full conversation between a student and an advisor, "
        "analyze it and fill the following JSON structure as accurately as possible:\n\n"
        "{\n"
        "  'portfolio_json': {\n"
        "    'name': '',\n"
        "    'highlighted_skills': [],\n"
        "    'interests': [],\n"
        "    'personality_traits': [],\n"
        "    'education_level': 'Class 11 Student',\n"
        "    'recommended_paths': [],\n"
        "    'next_steps': []\n"
        "  }\n"
        "}\n"
        "Make realistic, specific guesses from context — don’t overinflate."
    )

    response = call_shivaay_agent(system_prompt, text)
    return response
