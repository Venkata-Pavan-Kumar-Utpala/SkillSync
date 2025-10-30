import { configDotenv } from 'dotenv';
import express, { json } from 'express';
import cors from 'cors';
import axios from 'axios'; // We need axios to call the Python API
import { authMiddleware, getUserProfile } from "./middleware/authMiddleware.js";
const app = express();
const PORT = process.env.PORT || 8000;


// Mock User Data & Auth
// In a real app, this would come from a JWT token and MongoDB
app.use(authMiddleware); // Mock auth middleware
//

// URL of your Python ML/AI server
// Make sure it's running on a different port (e.g., 8001)
const ML_API_URL = process.env.ML_API_URL || 'http://localhost:8001';

app.use(cors()); // Allow requests from your React app
app.use(json());

/**
 * @route POST /api/chat
 * This is the main router for all 4 buttons.
 * It gets the user profile and then calls the appropriate
 * endpoint on the Python/FastAPI server.
 */
app.post('/api/chat', async (req, res) => {
  const { type, goal, query } = req.body;
  const userId = req.user.id; // Get user ID from our mock auth

  try {
    const userProfile = await getUserProfile(userId);
    if (!userProfile) {
      return res.status(404).json({ message: 'User profile not found.' });
    }

    // Convert profile to the JSON string format the ML API expects
    const portfolioJsonString = JSON.stringify(userProfile.profile);

    let result;

    switch (type) {
      case 'CAREER_RECOMMENDATION': {
        console.log('MERN: Calling Python /recommend-career endpoint...');
        const response = await axios.post(`${ML_API_URL}/recommend-career`, {
          portfolio_json: portfolioJsonString
        });
        result = response.data;
        break;
      }

      case 'SKILL_PATHWAY': {
        console.log('MERN: Calling Python /get-skill-pathway endpoint...');
        // TODO: Ask your ML teammate to add a '/get-skill-pathway' endpoint
        // It will likely need both the portfolio_json and a 'goal'
        // const response = await axios.post(`${ML_API_URL}/get-skill-pathway`, {
        //   portfolio_json: portfolioJsonString,
        //   goal: goal 
        // });
        // result = response.data;
        
        // Mock Data for Hackathon
        result = {
          pathway: [
            "Learn Python fundamentals.",
            "Master data analysis libraries: Pandas and NumPy.",
            "Build 3 projects using Scikit-learn.",
            "Learn data visualization with Tableau."
          ]
        };
        // End Mock Data
        break;
      }

      case 'COURSE_RECOMMENDATION': {
        console.log('MERN: Calling Python /get-courses endpoint...');
        // TODO: Ask your ML teammate to add a '/get-courses' endpoint
        // It will likely need the portfolio_json and a 'query' (e.g., "Python")
        // const response = await axios.post(`${ML_API_URL}/get-courses`, {
        //   portfolio_json: portfolioJsonString,
        //   skill: query // e.g., query = "Python"
        // });
        // result = response.data;
        
        // Mock Data for Hackathon
        result = {
          courses: [
            { name: "Complete Python Bootcamp", platform: "Udemy" },
            { name: "Google Data Analytics Certificate", platform: "Coursera" }
          ]
        };
        // End Mock Data
        break;
      }

      case 'PORTFOLIO_BUILDER': {
        console.log('MERN: Calling Python /get-portfolio-project endpoint...');
        // TODO: Ask your ML teammate to add a '/get-portfolio-project' endpoint
        // It will likely need the portfolio_json and a 'goal' (e.g., "Data Analyst")
        // const response = await axios.post(`${ML_API_URL}/get-portfolio-project`, {
        //   portfolio_json: portfolioJsonString,
        //   goal_role: goal 
        // });
        // result = response.data;
        
        // Mock Data for Hackathon
        result = {
          project_idea: {
            title: "Global COVID-19 Data Analysis",
            description: "Analyze and visualize the spread and impact of COVID-19 using a public dataset."
          }
        };
        // End Mock Data
        break;
      }

      default:
        return res.status(400).json({ message: 'Invalid request type' });
    }

    return res.json(result);

  } catch (error) {
    console.error('Error in /api/chat:', error.message);
    res.status(500).json({ message: 'Error processing your request.' });
  }
});

app.listen(PORT, () => {
  console.log(`MERN server (Express) is running on http://localhost:${PORT}`);
  console.log(`Make sure the Python AI server is running on ${ML_API_URL}`);
});
