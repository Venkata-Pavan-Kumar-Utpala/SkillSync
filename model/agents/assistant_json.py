from utils.shivaay_api import call_shivaay_agent

def assistant_json_formatter(data):
    system_prompt = (
        "You are AssistantJSON. You receive data and ensure it’s a clean, valid JSON format "
        "with clear keys and values. Do not add extra commentary."
    )
    return call_shivaay_agent(system_prompt, data)
