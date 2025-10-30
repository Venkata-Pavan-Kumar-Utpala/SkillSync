from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from agents.json_parser import parse_user_profile
from agents.assistant_json import assistant_json_formatter
from agents.summary_gen import generate_summary
from agents.career_recommender import recommend_career
from agents.topic_generator import generate_topics_from_portfolio
import requests
import os
import json

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "c49fedb8bdda42d8bf2adf138297ab0c")

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



@app.post("/get-job-trends")
async def get_job_trends(request: Request):
    """
    Fetch trending job market articles based on skill or keyword.
    """
    try:
        data = await request.json()
        skill = data.get("skill", "")
        if not skill:
            return {"error": "Please provide a skill or keyword"}

        url = f"https://newsapi.org/v2/everything?q={skill}+jobs&language=en&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        if response.status_code != 200:
            return {"error": "NewsAPI request failed", "status": response.status_code}

        articles = response.json().get("articles", [])
        results = [
            {
                "title": a["title"],
                "source": a["source"]["name"],
                "url": a["url"],
                "publishedAt": a["publishedAt"]
            }
            for a in articles
        ]
        return {"skill": skill, "job_trends": results}

    except Exception as e:
        return {"error": str(e)}


@app.post("/get-course-trends")
async def get_course_trends(request: Request):
    """
    Automatically generate trending topics from user portfolio,
    then fetch top 5 related articles using NewsAPI.
    """
    try:
        data = await request.json()
        portfolio_json = data.get("portfolio_json", {})

        # Generate trending topics using Shivaay
        topics = generate_topics_from_portfolio(portfolio_json)

        all_trends = []

        for topic in topics:
            url = (
                f"https://newsapi.org/v2/everything?q={topic}+courses+learning"
                f"&language=en&sortBy=popularity&pageSize=3&apiKey={NEWS_API_KEY}"
            )
            res = requests.get(url)
            if res.status_code == 200:
                articles = res.json().get("articles", [])
                formatted = [
                    {
                        "topic": topic,
                        "title": a["title"],
                        "source": a["source"]["name"],
                        "url": a["url"],
                        "publishedAt": a["publishedAt"],
                    }
                    for a in articles
                ]
                all_trends.extend(formatted)

        return {"topics": topics, "course_trends": all_trends}

    except Exception as e:
        return {"error": str(e)}