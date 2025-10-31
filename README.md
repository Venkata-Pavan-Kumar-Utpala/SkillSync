# 🎯 SkillSync - AI-Powered Career Path Recommender (Acelnt AI)

## 🚀 Overview
SkillSync is an **AI-powered career recommender API** built using **FastAPI**.  
It analyzes a student’s academic history, skills, and interests to recommend **personalized career paths**, **learning resources**, and **industry trends**.  
The project leverages AI agents for parsing, recommendation, and summarization, and integrates **real-time market insights** using the NewsAPI.

---

## 🧠 Core Features

### 🔹 User Profiling
Parses a student’s academic details, projects, and interests into a structured JSON profile.

### 🔹 Career Recommendation
Uses AI models to match user profiles with suitable career roles (like Data Analyst, Product Manager, UX Designer, etc.).

### 🔹 Smart Summaries
Generates summarized insights from the user’s portfolio or chat conversation.

### 🔹 Job Trends
Fetches trending articles about job market demand and skills using **NewsAPI**.

### 🔹 Course Trends
Generates trending learning topics from a user’s portfolio and fetches related resources and articles.

### 🔹 Portfolio Builder (Planned)
Creates structured portfolios dynamically based on user interactions.

---

## 🏗️ Implementation Logic

- **Frontend** sends user input → `/parse-profile`  
- **Backend** parses it into JSON via AI agents → `/generate-json`  
- **Career suggestions** generated using `/recommend-career`  
- **Trending jobs & courses** fetched via NewsAPI → `/get-job-trends` & `/get-course-trends`  
- **Summary generation** from conversation history → `/get-summary`  
- All endpoints are cross-origin enabled for frontend communication.

---

## ⚙️ Setup and Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd career-recommender-api
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install fastapi uvicorn requests python-dotenv
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```env
NEWS_API_KEY=your_newsapi_key_here
```

Get your NewsAPI key from: https://newsapi.org/

## 🚀 Running the Application

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The API will be available at:
- **Local**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 API Endpoints

### 1. Health Check
```
GET /
```
Returns API status message.

**Response:**
```json
{
  "message": "Career Recommender API is running!"
}
```

---

### 2. Generate Portfolio JSON
```
POST /generate-json
```
Converts user text input into structured portfolio JSON.

**Request Body:**
```json
{
  "text": "I am a software engineer with 5 years of experience in Python..."
}
```

**Response:**
```json
{
  "portfolio_json": { /* structured portfolio data */ }
}
```

---

### 3. Get Conversation Summary
```
POST /get-summary
```
Generates a concise summary from conversation history.

**Request Body:**
```json
{
  "conversation": "User: I want to become a data scientist...\nAssistant: Great! Let's discuss..."
}
```

**Response:**
```json
{
  "summary": "User is interested in transitioning to data science..."
}
```

---

### 4. Recommend Career
```
POST /recommend-career
```
Provides personalized career recommendations based on portfolio.

**Request Body:**
```json
{
  "portfolio_json": {
    "skills": ["Python", "Machine Learning"],
    "experience": "3 years",
    "education": "Computer Science"
  }
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "career": "Data Scientist",
      "match_score": 0.85,
      "reasons": ["Strong Python skills", "ML background"]
    }
  ]
}
```

---

### 5. Parse User Profile
```
POST /parse-profile
```
Extracts structured information from raw user input.

**Request Body:**
```json
{
  "user_input": "I'm a 25-year-old developer interested in AI and cloud computing..."
}
```

**Response:**
```json
{
  "parsed_json": {
    "age": 25,
    "current_role": "developer",
    "interests": ["AI", "cloud computing"]
  }
}
```

---

### 6. Get Job Market Trends
```
POST /get-job-trends
```
Fetches latest job market articles for a specific skill.

**Request Body:**
```json
{
  "skill": "React"
}
```

**Response:**
```json
{
  "skill": "React",
  "job_trends": [
    {
      "title": "Top React Developer Jobs in 2025",
      "source": "TechCrunch",
      "url": "https://...",
      "publishedAt": "2025-10-30T10:00:00Z"
    }
  ]
}
```

---

### 7. Get Course Trends
```
POST /get-course-trends
```
Automatically generates relevant topics from portfolio and finds trending courses.

**Request Body:**
```json
{
  "portfolio_json": {
    "skills": ["JavaScript", "React"],
    "interests": ["Web Development"]
  }
}
```

**Response:**
```json
{
  "topics": ["Advanced React Patterns", "JavaScript Performance"],
  "course_trends": [
    {
      "topic": "Advanced React Patterns",
      "title": "Master React Hooks and Patterns",
      "source": "Udemy News",
      "url": "https://...",
      "publishedAt": "2025-10-29T14:00:00Z"
    }
  ]
}
```

## 🏗️ Project Structure

```
career-recommender-api/
├── main.py                          # FastAPI application entry point
├── agents/                          # AI agent modules
│   ├── rec_newbie_career.py        # Career recommendation for beginners
│   ├── json_parser.py              # User profile parser
│   ├── assistant_json.py           # JSON formatter
│   ├── summary_gen.py              # Conversation summarizer
│   ├── career_recommender.py       # Career recommendation engine
│   ├── topic_generator.py          # Topic generation from portfolio
│   └── portfolio_builder.py        # Portfolio builder from conversation
├── .env                             # Environment variables
└── requirements.txt                 # Python dependencies
```

## 🔒 CORS Configuration

Currently set to allow all origins (`"*"`). For production, restrict to your frontend URL:

```python
allow_origins=["https://your-frontend-domain.com"]
```

## 🧪 Testing

Use the interactive API documentation at http://localhost:8000/docs to test all endpoints.

Or use curl:
```bash
curl -X POST "http://localhost:8000/recommend-career" \
  -H "Content-Type: application/json" \
  -d '{"portfolio_json": {"skills": ["Python", "Data Analysis"]}}'
```

## 🤝 Integration with Frontend

This API is designed to work with the SkillSync frontend application. Ensure your frontend makes requests to the correct API endpoints.

Example frontend integration:
```javascript
const response = await fetch('http://localhost:8000/recommend-career', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ portfolio_json: userPortfolio })
});
const data = await response.json();
```

## 📝 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEWS_API_KEY` | NewsAPI.org API key for fetching articles | Yes |
- Add authentication/authorization
- Implement rate limiting
- Add database for storing user portfolios
- Cache frequent requests
- Add more AI agents for specialized tasks
- WebSocket support for real-time updates
