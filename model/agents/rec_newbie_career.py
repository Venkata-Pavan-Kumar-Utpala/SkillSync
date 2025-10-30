from utils.shivaay_api import call_shivaay_agent
import json

def rec_newbie_career(conversation_history=""):
    """
    For students with no prior experience or clear direction.
    Shivaay acts as an interactive counselor:
    - Asks questions to infer interests, values, and strengths
    - Fills a JSON-like portfolio
    - Then recommends career paths based on inferred personality and skills
    """

    system_prompt = (
        "You are an empathetic AI career counselor helping a high-school student (class 11). "
        "They have no defined career path or clear strengths yet. "
        "Your goal is to ask short, friendly questions to understand their personality, interests, learning style, and values. "
        "After gathering enough details, summarize their potential strengths and fill a portfolio in JSON format with the following structure:\n\n"
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
        "}\n\n"
        "Be realistic and supportive. Avoid being overly optimistic or harsh. "
        "If the student is unsure, infer possible directions based on their responses. "
        "After filling the JSON, also recommend 3-5 suitable career domains and how to start exploring them."
    )

    user_prompt = (
        "The following is a partial or ongoing conversation with a student about their interests. "
        "Based on this conversation, infer missing details and produce a completed portfolio JSON and recommendations.\n\n"
        f"{conversation_history}"
    )

    result = call_shivaay_agent(system_prompt, user_prompt)

    # Try to cleanly parse JSON from the response
    try:
        parsed = json.loads(result)
    except Exception:
        parsed = {"raw_response": result}

    return parsed
