import express from 'express';
import cors from 'cors';
import axios from 'axios';
import { randomUUID } from 'crypto'; // Import crypto for generating session IDs

// --- CONFIGURATION ---
const app = express();
const PORT = process.env.PORT || 8000;
// This is the URL of your Python/FastAPI server
const PYTHON_API_URL = process.env.PYTHON_API_URL || 'http://localhost:8001';

// --- MIDDLEWARE ---
app.use(cors()); // Allow cross-origin requests (from your React frontend)
app.use(express.json()); // Parse incoming JSON bodies

// --- API ENDPOINTS ---

/**
 * Main chat/logic endpoint.
 * Acts as a proxy to the Python ML server.
 */
app.post('/api/chat', async (req, res) => {
  // Get the button type and profile data from the frontend
  const { type, profile } = req.body;

  // We are no longer using the mock user, so the 'profile' object from
  // the request (e.g., from Postman or your React app) is our source of truth.
  if (!profile) {
    return res.status(400).json({ message: 'Profile data is missing.' });
  }

  let result;
  let response;

  // Log exactly what profile we are about to use
  console.log(`Handling ${type} with profile:`, JSON.stringify(profile));

  try {
    switch (type) {
      // --- Case 1: Career Recommendation ---
      case 'CAREER_RECOMMENDATION':
        response = await axios.post(`${PYTHON_API_URL}/recommend-career`, {
          portfolio_json: JSON.stringify(profile), // Send the full profile
        });
        result = response.data;
        break;
      
      // --- Case 2: Course Recommendation ---
      case 'COURSE_RECOMMENDATION':
        response = await axios.post(`${PYTHON_API_URL}/get-course-trends`, {
          portfolio_json: profile, // This endpoint expects a JSON object
        });
        result = response.data;
        break;

      // --- Case 3: Portfolio Builder (NEW!) ---
      // This button will now use your new conversational agent
      case 'PORTFOLIO_BUILDER':
        // 1. Convert the profile object into a single string to start the "conversation"
        const firstMessage = `Here is my profile: ${JSON.stringify(profile)}`;
        
        // 2. Generate a unique session ID for the conversation memory
        const sessionId = randomUUID();

        // 3. Call the new /rec-newbie-career endpoint
        response = await axios.post(`${PYTHON_API_URL}/rec-newbie-career`, {
          conversation: firstMessage,
          session_id: sessionId
        });
        
        // This endpoint returns a complex object, which is great!
        // We'll just send the whole thing to the frontend.
        result = response.data;
        break;

      // --- Case 4: Skill Pathway (Not yet implemented in Python) ---
      case 'SKILL_PATHWAY':
        result = {
          recommendations: "The **Skill Pathway** agent is not yet connected. Please ask the ML team to create a Python endpoint for this button.",
        };
        break;

      default:
        return res.status(400).json({ message: 'Invalid request type' });
    }

    // Send the successful result (from Python) back to the frontend
    return res.status(200).json(result);

  } catch (error) {
    // Handle errors
    console.error(`Error in /api/chat for type ${type}:`, error.message);
    if (error.response) {
      // The request was made and the server responded with a non-2xx status
      console.error('Python Server Error:', error.response.data);
    } else if (error.request) {
      // The request was made but no response was received (e.g., Python server is down)
      console.error('No response from Python server:', error.request);
    }
    return res.status(500).json({ message: 'Error processing your request.' });
  }
});

/**
 * News endpoint.
 * Fetches job trends from the Python server.
 */
app.post('/api/news', async (req, res) => {
  const { skill } = req.body;
  if (!skill) {
    return res.status(400).json({ message: 'Skill is required' });
  }

  try {
    const response = await axios.post(`${PYTHON_API_URL}/get-job-trends`, {
      skill: skill,
    });
    return res.status(200).json(response.data);
  } catch (error) {
    console.error('Error in /api/news:', error.message);
    return res.status(500).json({ message: 'Error fetching news.' });
  }
});

// --- START SERVER ---
app.listen(PORT, () => {
  console.log(`MERN Backend Server is running on http://localhost:${PORT}`);
  console.log(`Proxying ML requests to: ${PYTHON_API_URL}`);
});

