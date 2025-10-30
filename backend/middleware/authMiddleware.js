const mockUser = {
  _id: 'user123',
  email: 'demo@example.com',
  isFirstLogin: false,
  profile: {
    fullName: "Demo User",
    education: [
      {
        institution: "State University",
        degree: "B.S. in Computer Science",
        year: "2024"
      }
    ],
    projects: [
      {
        name: "E-commerce Website",
        description: "Built a full-stack e-commerce site with React and Node.js."
      }
    ],
    skills: ["React", "Node.js", "MongoDB", "JavaScript", "Python"],
    mbti: "INTJ",
    interests: ["Artificial Intelligence", "Web Development", "Chess"]
  }
};

// Mock middleware to add user to req
const authMiddleware = (req, res, next) => {
  req.user = { id: mockUser._id };
  next();
};

// Mock DB call
const getUserProfile = async (userId) => {
  if (userId === mockUser._id) {
    return mockUser;
  }
  return null;
};

export { authMiddleware, getUserProfile }
