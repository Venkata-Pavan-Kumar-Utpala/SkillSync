from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agents.json_parser import parse_user_profile
from agents.assistant_json import assistant_json_formatter
from agents.summary_gen import generate_summary
from agents.career_recommender import recommend_career
import json


app = FastAPI(title="Career Recommender API", version="1.0")

# Allow your teammates’ frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Career Recommender API is running!"}

@app.post("/generate-json")
async def generate_json(request: Request):
    data = await request.json()
    user_text = data.get("text", "")
    parsed = parse_user_profile(user_text)
    formatted = assistant_json_formatter(parsed)
    return {"portfolio_json": formatted}

@app.post("/get-summary")
async def get_summary(request: Request):
    data = await request.json()
    conversation = data.get("conversation", "")
    summary = generate_summary(conversation)
    return {"summary": summary}

@app.post("/recommend-career")
async def recommend_career_endpoint(request: Request):
    data = await request.json()
    user_json = data.get("portfolio_json", "")
    recommendations = recommend_career(user_json)
    if isinstance(user_json, dict):
        user_json = json.dumps(user_json)

    try:
        recommendations = recommend_career(user_json)
        return {"recommendations": recommendations}
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/parse-profile")
async def parse_profile_endpoint(request: Request):
    try:

        data = await request.json()
        user_input = data.get("user_input", "")
        parsed_json = parse_user_profile(user_input)

        if isinstance(parsed_json, str):
            try:
                parsed_json = json.loads(parsed_json)
            except json.JSONDecodeError:
                parsed_json = {"raw_response": parsed_json}

        return {"parsed_json": parsed_json}
    except Exception as e:
        return {"error": str(e)}


