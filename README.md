# Interview Coach - AI-Powered Communication & Interview Coaching System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571.svg?style=flat)](https://fastapi.tiangolo.com/)

## Overview

Interview Coach is an AI-powered system designed to help candidates improve their interview skills through personalized feedback, intelligent analysis, and progress tracking. The system uses a multi-agent architecture to provide comprehensive, actionable feedback on interview responses.

## Features

### Core Capabilities

- **Interview Question Database**: 100+ questions across various roles, competencies, and difficulty levels
- **Multi-Agent Analysis**: 5 specialized AI agents for comprehensive feedback
- **Personalized Coaching**: Tailored recommendations based on your performance
- **Progress Tracking**: Monitor improvement over time with detailed analytics
- **Voice Support**: Record and transcribe voice responses (experimental)
- **STAR Method**: Learn and practice the Situation-Task-Action-Result framework

### Multi-Agent System

1. **Question Agent**: Selects appropriate questions based on your role and competencies
2. **Communication Agent**: Evaluates clarity, structure, and professional tone
3. **Content Agent**: Assesses relevance, completeness, and knowledge depth
4. **STAR Agent**: Analyzes responses using the STAR framework
5. **Coach Agent**: Consolidates feedback and generates improvement plans

### User Features

- **Practice Mode**: Answer questions and get instant feedback
- **History**: Review past practice sessions
- **Progress Dashboard**: Visualize improvement over time
- **Profile Management**: Customize your candidate profile
- **Follow-up Questions**: Dig deeper into specific topics

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   React         │────▶│   FastAPI       │────▶│   SQLite        │
│   Frontend      │     │   Backend       │     │   Database      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                       │
         │                       ▼                       │
         │             ┌─────────────────┐              │
         │             │ Multi-Agent     │              │
         │             │ System          │◀─────────────┘
         │             └─────────────────┘
         │                       │
         │                       ▼
         │             ┌─────────────────┐
         └────────────▶│   LLM Provider   │
                        │ (OmniRoute/Kiro)│
                        └─────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Node.js 16 or higher
- Git
- SQLite (included with Python)

### Installation

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd interview-coach
```

#### 2. Set Up Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your settings
nano .env  # or use your preferred editor

# Initialize database
python -c "from database import init_db; import asyncio; asyncio.run(init_db())"
```

#### 3. Set Up Frontend

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Edit .env with your API URL
nano .env
```

#### 4. Configure LLM Provider

Edit the backend `.env` file and add your LLM API keys:

```bash
OMNIROUTE_API_KEY=your-omniroute-api-key
KIRO_LLM_API_KEY=your-kiro-llm-api-key
```

> **Note**: The system includes mock LLM responses for development. You can test without API keys, but for full functionality, you'll need to provide valid API keys.

### Running the Application

#### Development Mode

**Backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- API Docs: http://localhost:8000/api/docs

#### Production Mode

**Backend:**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm run build
# Serve the build folder with a web server like nginx or serve
npx serve -s build -l 3000
```

## Usage

### 1. Register and Login

1. Visit http://localhost:3000
2. Click "Get Started Free" or "Sign Up"
3. Create your account
4. Login with your credentials

### 2. Create Your Profile

1. After login, navigate to Profile page
2. Fill in your candidate information:
   - Target role (e.g., "Software Engineer")
   - Years of experience
   - Skills (comma separated)
   - Competencies (comma separated)
   - Resume/Bio

### 3. Start Practicing

1. Go to the Practice page
2. Click "Start Practicing" or select a specific category
3. A question will be displayed
4. Type your response or click "Record Voice" to record an audio response
5. Click "Get Full Analysis" to receive comprehensive feedback

### 4. Review Feedback

After submitting your response, you'll see:
- **Overall Score**: Composite score from all agents
- **Agent Scores**: Individual scores from each specialist agent
- **Strengths**: What you did well
- **Areas for Improvement**: Where you can improve
- **Suggestions**: Actionable recommendations
- **Follow-up Questions**: Questions to dig deeper
- **Improved Response**: Example of how to improve your answer

### 5. Track Progress

1. Visit the Progress page to see:
   - Overall performance trends
   - Scores by competency and area
   - Improvement over time
   - Personalized recommendations

2. Visit the History page to:
   - Review past practice sessions
   - Filter by date, role, or question type
   - View detailed feedback for each response

## API Documentation

Full API documentation is available in the `docs/API_DOCUMENTATION.md` file.

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/token` | Login and get JWT token |
| GET | `/candidates/me` | Get current candidate profile |
| POST | `/agents/practice/start` | Start a new practice session |
| POST | `/feedback/analyze` | Analyze a response with multi-agent system |
| GET | `/progress/candidate/{id}/summary` | Get progress summary |

## Project Structure

```
interview-coach/
├── backend/                  # FastAPI Backend
│   ├── main.py               # Application entry point
│   ├── config/               # Configuration files
│   ├── database.py           # Database setup
│   ├── models/               # Pydantic models
│   ├── schemas/              # Response schemas
│   ├── services/             # Business logic
│   ├── routers/              # API routes
│   ├── agents/               # Multi-agent system
│   └── requirements.txt      # Python dependencies
│
├── frontend/                 # React Frontend
│   ├── public/               # Static files
│   ├── src/                  # Source files
│   │   ├── App.js            # Main application
│   │   ├── index.js          # Entry point
│   │   ├── components/       # UI components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API services
│   │   ├── context/          # React context
│   │   └── utils/            # Utility functions
│   └── package.json          # npm dependencies
│
├── docs/                    # Documentation
│   ├── ARCHITECTURE.md       # System architecture
│   └── API_DOCUMENTATION.md # API documentation
│
├── .env.example             # Example environment file
├── .gitignore               # Git ignore patterns
└── README.md                # This file
```

## Multi-Agent System Details

### Agent Types

1. **Question Agent**
   - Selects questions based on role, competency, difficulty
   - Generates follow-up questions
   - Supports random and targeted question selection

2. **Communication Agent**
   - Evaluates clarity, structure, conciseness
   - Assesses professional tone
   - Provides actionable suggestions
   - Uses hybrid scoring (rule-based + LLM)

3. **Content Agent**
   - Assesses relevance to the question
   - Evaluates completeness
   - Measures knowledge depth
   - Checks for experience demonstration

4. **STAR Agent**
   - Identifies Situation, Task, Action, Result components
   - Scores each STAR element
   - Provides STAR method examples
   - Suggests improvements to STAR structure

5. **Coach Agent**
   - Consolidates all agent feedback
   - Identifies recurring patterns
   - Generates personalized recommendations
   - Creates improvement plans
   - Provides motivational feedback

### Agent Workflow

```
User Response
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│                    ANALYSIS PHASE                           │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ Communication│  │   Content   │  │     STAR    │    │
│  │    Agent     │  │    Agent    │  │    Agent    │    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
│         │                 │                 │            │
│         └─────────────────┼─────────────────┘            │
│                           │                                │
│                           ▼                                │
│              ┌─────────────────────────┐                  │
│              │      COACH AGENT        │                  │
│              │  (Consolidation)        │                  │
│              └──────────┬────────────┘                  │
│                         │                                    │
└─────────────────────────┼────────────────────────────────┘
                          │
                          ▼
              ┌─────────────────────────┐
              │      FEEDBACK           │
              │  - Overall Score        │
              │  - Performance Summary  │
              │  - Agent Scores         │
              │  - Strengths/Weaknesses  │
              │  - Recommendations      │
              │  - Follow-up Questions   │
              │  - Improved Response     │
              └─────────────────────────┘
```

## Database Schema

The system uses SQLite with the following tables:

- **users**: User authentication and profiles
- **candidates**: Candidate information for coaching
- **questions**: Interview questions database
- **sessions**: Practice sessions
- **responses**: User responses to questions
- **feedback**: Detailed feedback on responses
- **progress**: Progress tracking over time
- **api_keys**: LLM API key storage

See `backend/database.py` for the complete schema.

## Configuration

### Environment Variables

#### Backend (`.env`)

```bash
# Application
APP_NAME=Interview Coach API
APP_VERSION=1.0.0
DEBUG=True
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=sqlite:///interview_coach.db

# LLM Configuration
OMNIROUTE_API_KEY=your-omniroute-api-key
KIRO_LLM_API_KEY=your-kiro-llm-api-key
DEFAULT_LLM_PROVIDER=omniroute
DEFAULT_MODEL=kiro

# File Uploads
UPLOAD_DIR=uploads
AUDIO_UPLOAD_DIR=uploads/audio
MAX_UPLOAD_SIZE=10485760  # 10MB

# CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

#### Frontend (`.env`)

```bash
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_NAME=Interview Coach
```

## Testing

### Backend Tests

```bash
cd backend
python -m pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Deployment

### Docker (Optional)

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=sqlite:////app/interview_coach.db
    command: uvicorn main:app --host 0.0.0.0 --port 8000

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
    environment:
      - REACT_APP_API_URL=http://backend:8000/api
    depends_on:
      - backend
```

Then run:

```bash
docker-compose up --build
```

### Manual Deployment

1. **Backend**: Deploy to any Python hosting (e.g., Heroku, AWS, DigitalOcean)
2. **Frontend**: Build and deploy static files to any web hosting
3. **Database**: Use SQLite for development, PostgreSQL/MySQL for production

## Troubleshooting

### Common Issues

1. **Database not initializing**
   - Ensure SQLite is installed
   - Check file permissions
   - Run `python -c "from database import init_db; import asyncio; asyncio.run(init_db())"` manually

2. **CORS errors**
   - Ensure `CORS_ORIGINS` in backend settings includes your frontend URL
   - Check that the frontend is using the correct API URL

3. **LLM API errors**
   - Verify your API keys are correct
   - Check your account balance/quota with the LLM provider
   - Use mock mode for development (remove API key to enable)

4. **Authentication errors**
   - Ensure you're sending the JWT token in the Authorization header
   - Verify token hasn't expired (30 minutes)
   - Login again to get a new token

### Debug Mode

Enable debug mode in backend `.env`:

```bash
DEBUG=True
```

This will provide more detailed error messages and logging.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

### Code Style

- **Python**: Follow PEP 8 guidelines
- **JavaScript**: Use ESLint configuration from the project
- **Commits**: Use descriptive commit messages
- **Tests**: Add tests for new features

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [React](https://reactjs.org/) - Frontend library
- [Bootstrap](https://getbootstrap.com/) - CSS framework
- [Recharts](https://recharts.org/) - Charting library
- [OmniRoute](https://omniroute.com/) - LLM provider
- [Kiro](https://kiro.ai/) - LLM provider

## Contact

For questions or support, please contact the project maintainers.

---

**Interview Coach** - Helping you ace your next interview with AI-powered coaching.

*Built with ❤️ for better interviews*
