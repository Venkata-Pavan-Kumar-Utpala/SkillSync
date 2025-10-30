from utils.shivaay_api import call_shivaay_agent

def generate_summary(conversation_text):
    system_prompt = (
        "You are SummaryGen. Your job is to create a concise and meaningful summary "
        "of the session or user data provided. Keep it under 100 words."
    )
    return call_shivaay_agent(system_prompt, conversation_text)
