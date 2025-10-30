import express from 'express';
import cors from 'cors';
import axios from 'axios';
// We remove authMiddleware and getUserProfile for testing
// import { authMiddleware, getUserProfile } from './middleware/authMiddleware.js';

const app = express();
const PORT = process.env.PORT || 8000;

const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:8001';

// Middleware
app.use(cors());
app.use(express.json());

/**
 * Main Chat Endpoint
 * This single endpoint routes all button clicks to the correct Python service.
 */
// We remove the 'authMiddleware' from the route to make testing easier
app.post('/api/chat', async (req, res) => {
  // Get the 'type' and 'profile' directly from the Postman request body
  const { type, profile } = req.body;
  
  // --- THIS IS THE FIX ---
  // Instead of merging with a mock user, we will ONLY use the profile
  // sent from Postman. This ensures your changes are respected.
  const fullUserProfile = profile;
  // -----------------------

  // Convert the profile into the JSON string format the Python server expects
  const portfolioJsonString = JSON.stringify(fullUserProfile);

  let response;
  try {
    switch (type) {
      case 'CAREER_RECOMMENDATION':
        console.log('Handling Career Recommendation with profile:', portfolioJsonString);
        response = await axios.post(`${PYTHON_API_URL}/recommend-career`, {
          portfolio_json: portfolioJsonString
        });
        break;

      case 'SKILL_PATHWAY':
        console.log('Handling Skill Pathway...');
        response = { data: { recommendations: `**Skill Pathway Logic (Not Implemented in Python Yet)**\n\nBased on your goal, here is a mock path:\n1. Learn Python\n2. Master Pandas\n3. Build a project` } };
        break;

      case 'COURSE_RECOMMENDATION':
        console.log('Handling Course Recommendation with profile:', JSON.stringify(fullUserProfile));
        response = await axios.post(`${PYTHON_API_URL}/get-course-trends`, {
          portfolio_json: fullUserProfile // This endpoint takes the full JSON object
        });
        break;

      case 'PORTFOLIO_BUILDER':
        console.log('Handling Portfolio Builder...');
        response = { data: { recommendations: `**Portfolio Builder Logic (Not Implemented in Python Yet)**\n\nHere is a mock project idea:\n\nBuild a personal finance tracker using React and Plaid API.` } };
        break;

      default:
        return res.status(400).json({ message: 'Invalid request type' });
    }

    res.json(response.data);

  } catch (error) {
    console.error(`Error in /api/chat:`, error.message);
    res.status(500).json({ message: 'Error processing your request.' });
  }
});

/**
 * News/Trends Endpoint
 */
// We remove 'authMiddleware' here too for simple testing
app.post('/api/news', async (req, res) => {
  const { skill } = req.body;
  try {
    console.log(`Fetching news for skill: ${skill}`);
    const response = await axios.post(`${PYTHON_API_URL}/get-job-trends`, {
      skill: skill
    });
    res.json(response.data);
  } catch (error) {
    console.error(`Error in /api/news:`, error.message);
    res.status(500).json({ message: 'Error fetching job trends.' });
  }
});


// Start the server
app.listen(PORT, () => {
  console.log(`MERN Backend Server is running on http://localhost:${PORT}`);
});

