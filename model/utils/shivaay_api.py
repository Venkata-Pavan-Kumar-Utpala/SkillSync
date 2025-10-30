import requests

# ✅ Correct base URL (not /lara/)
API_URL = "https://api.futurixai.com/api/shivaay/v1/chat/completions"
API_KEY = "69033fd63bb9326d465663fc"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

def call_shivaay_agent(system_prompt, user_prompt, temperature=0.4, max_tokens=500):
    """
    Sends a chat completion request to FuturixAI Shivaay API.
    Compatible with OpenAI-style message format.
    """
    payload = {
        "model": "shivaay",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    try:
        res = requests.post(API_URL, headers=HEADERS, json=payload)
        res.raise_for_status()  # raises exception if status != 200
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error: {e}")

    try:
        data = res.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        raise Exception(f"Unexpected response: {res.text}")
