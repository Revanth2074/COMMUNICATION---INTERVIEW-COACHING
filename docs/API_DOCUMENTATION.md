# Interview Coach - API Documentation

## Base URL

```
http://localhost:8000/api
```

## Authentication

All endpoints (except `/auth/register` and `/auth/token`) require authentication via JWT Bearer token.

### Token Format

```
Authorization: Bearer <token>
```

### Token Expiration

Tokens expire after 30 minutes. Users must login again to get a new token.

---

## Authentication Endpoints

### Register User

**Endpoint:** `POST /auth/register`

**Description:** Create a new user account

**Request Body:**
```json
{
  "username": "string (required)",
  "email": "string (required)",
  "full_name": "string (optional)",
  "password": "string (required, min 6 characters)"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe"
  }
}
```

### Login (Get Token)

**Endpoint:** `POST /auth/token`

**Content-Type:** `application/x-www-form-urlencoded`

**Request Body:**
```
username: string (required)
password: string (required)
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "is_admin": false
  }
}
```

### Get Current User

**Endpoint:** `GET /auth/me`

**Description:** Get information about the currently authenticated user

**Response:**
```json
{
  "success": true,
  "message": "Current user retrieved successfully",
  "data": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "is_admin": false,
    "created_at": "2024-01-01T00:00:00"
  }
}
```

### Save API Key

**Endpoint:** `POST /auth/api-keys`

**Query Parameters:**
- `service_name`: string (required) - e.g., "omniroute"
- `api_key`: string (required) - Your API key

**Response:**
```json
{
  "success": true,
  "message": "API key saved successfully",
  "data": {
    "service": "omniroute",
    "user_id": 1
  }
}
```

---

## Candidate Endpoints

### Create Candidate

**Endpoint:** `POST /candidates/`

**Request Body:**
```json
{
  "user_id": "string (required)",
  "name": "string (required)",
  "email": "string (required)",
  "target_role": "string (required)",
  "experience_years": 0,
  "skills": ["string"],
  "competencies": ["string"],
  "resume_text": "string (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Candidate created successfully",
  "data": {
    "id": 1,
    "user_id": "user_123",
    "name": "John Doe",
    "email": "john@example.com",
    "target_role": "Software Engineer",
    "experience_years": 5,
    "skills": ["Python", "FastAPI"],
    "competencies": ["Problem Solving"],
    "resume_text": "...",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

### Get Candidate

**Endpoint:** `GET /candidates/{candidate_id}`

**Response:**
```json
{
  "success": true,
  "message": "Candidate retrieved successfully",
  "data": {
    "id": 1,
    "user_id": "user_123",
    "name": "John Doe",
    "email": "john@example.com",
    "target_role": "Software Engineer",
    "experience_years": 5,
    "skills": ["Python", "FastAPI"],
    "competencies": ["Problem Solving"],
    "resume_text": "...",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

### Get Current Candidate

**Endpoint:** `GET /candidates/me`

**Response:** Same as Get Candidate

### Get All Candidates

**Endpoint:** `GET /candidates/`

**Query Parameters:**
- `page`: integer (default: 1)
- `page_size`: integer (default: 10, max: 100)

**Response:**
```json
{
  "success": true,
  "message": "Candidates retrieved successfully",
  "data": [
    {
      "id": 1,
      "user_id": "user_123",
      "name": "John Doe",
      "email": "john@example.com",
      "target_role": "Software Engineer",
      "experience_years": 5,
      "skills": ["Python", "FastAPI"],
      "competencies": ["Problem Solving"],
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10
}
```

### Update Candidate

**Endpoint:** `PUT /candidates/{candidate_id}`

**Request Body:**
```json
{
  "name": "string (optional)",
  "email": "string (optional)",
  "target_role": "string (optional)",
  "experience_years": 0,
  "skills": ["string"],
  "competencies": ["string"],
  "resume_text": "string (optional)"
}
```

**Response:** Same as Get Candidate

### Delete Candidate

**Endpoint:** `DELETE /candidates/{candidate_id}`

**Response:**
```json
{
  "success": true,
  "message": "Candidate deleted successfully",
  "data": null
}
```

---

## Question Endpoints

### Create Question

**Endpoint:** `POST /questions/`

**Request Body:**
```json
{
  "question_text": "string (required)",
  "role": "string (required)",
  "competency": "string (required)",
  "difficulty": "easy|medium|hard (default: medium)",
  "question_type": "string (required)",
  "expected_competency": "string (required)",
  "evaluation_criteria": ["string"],
  "category": "string (default: general)",
  "is_active": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Question created successfully",
  "data": {
    "id": 1,
    "question_text": "Tell me about yourself.",
    "role": "Software Engineer",
    "competency": "Communication",
    "difficulty": "easy",
    "question_type": "behavioral",
    "expected_competency": "Clear and concise self-introduction",
    "evaluation_criteria": ["Clarity", "Relevance", "Structure"],
    "category": "general",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00"
  }
}
```

### Get Question

**Endpoint:** `GET /questions/{question_id}`

**Response:** Same as Create Question response

### Get All Questions

**Endpoint:** `GET /questions/`

**Query Parameters:**
- `page`: integer (default: 1)
- `page_size`: integer (default: 10, max: 100)
- `role`: string (optional)
- `competency`: string (optional)
- `difficulty`: string (optional)
- `question_type`: string (optional)
- `category`: string (optional)

**Response:**
```json
{
  "success": true,
  "message": "Questions retrieved successfully",
  "data": [
    {
      "id": 1,
      "question_text": "Tell me about yourself.",
      "role": "Software Engineer",
      "competency": "Communication",
      "difficulty": "easy",
      "question_type": "behavioral",
      "expected_competency": "Clear and concise self-introduction",
      "evaluation_criteria": ["Clarity", "Relevance", "Structure"],
      "category": "general",
      "is_active": true,
      "created_at": "2024-01-01T00:00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10
}
```

### Get Random Question

**Endpoint:** `GET /questions/random`

**Query Parameters:**
- `role`: string (optional)
- `competency`: string (optional)
- `difficulty`: string (optional, default: medium)

**Response:** Same as Get Question response

### Get Questions by Role

**Endpoint:** `GET /questions/roles`

**Query Parameters:**
- `role`: string (required)

**Response:**
```json
{
  "success": true,
  "message": "Questions for role 'Software Engineer' retrieved successfully",
  "data": [...],
  "total": 10,
  "page": 1,
  "page_size": 100
}
```

### Get Question Statistics

**Endpoint:** `GET /questions/stats`

**Response:**
```json
{
  "success": true,
  "message": "Question statistics retrieved successfully",
  "data": {
    "by_role": {
      "Software Engineer": 25,
      "Product Manager": 15,
      "Data Scientist": 10
    },
    "by_competency": {
      "Communication": 20,
      "Problem Solving": 18,
      "Technical": 12
    },
    "by_difficulty": {
      "easy": 15,
      "medium": 25,
      "hard": 10
    },
    "by_type": {
      "behavioral": 20,
      "technical": 15,
      "situational": 10
    }
  }
}
```

### Update Question

**Endpoint:** `PUT /questions/{question_id}`

**Request Body:** Same as Create Question (all fields optional)

**Response:** Same as Get Question response

### Delete Question

**Endpoint:** `DELETE /questions/{question_id}`

**Response:**
```json
{
  "success": true,
  "message": "Question deleted successfully",
  "data": null
}
```

---

## Session Endpoints

### Create Session

**Endpoint:** `POST /sessions/`

**Request Body:**
```json
{
  "candidate_id": 1 (required),
  "question_id": 1 (required),
  "session_type": "practice|mock|evaluation (default: practice)",
  "status": "in_progress|completed (default: in_progress)"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Session created successfully",
  "data": {
    "id": 1,
    "candidate_id": 1,
    "question_id": 1,
    "session_type": "practice",
    "status": "in_progress",
    "started_at": "2024-01-01T00:00:00",
    "completed_at": null
  }
}
```

### Get Session

**Endpoint:** `GET /sessions/{session_id}`

**Response:** Same as Create Session response

### Get All Sessions

**Endpoint:** `GET /sessions/`

**Query Parameters:**
- `page`: integer (default: 1)
- `page_size`: integer (default: 10, max: 100)

**Response:**
```json
{
  "success": true,
  "message": "Sessions retrieved successfully",
  "data": [...],
  "total": 1,
  "page": 1,
  "page_size": 10
}
```

### Get Sessions by Candidate

**Endpoint:** `GET /sessions/candidate/{candidate_id}`

**Query Parameters:**
- `page`: integer (default: 1)
- `page_size`: integer (default: 10, max: 100)

**Response:** Same as Get All Sessions

### Get Session Details

**Endpoint:** `GET /sessions/{session_id}/details`

**Response:**
```json
{
  "success": true,
  "message": "Session details retrieved successfully",
  "data": {
    "session": {...},
    "candidate": {...},
    "question": {...}
  }
}
```

### Get Active Session

**Endpoint:** `GET /sessions/active/{candidate_id}`

**Response:** Same as Get Session response

### Complete Session

**Endpoint:** `POST /sessions/{session_id}/complete`

**Response:** Same as Get Session response (with updated status)

### Delete Session

**Endpoint:** `DELETE /sessions/{session_id}`

**Response:**
```json
{
  "success": true,
  "message": "Session deleted successfully",
  "data": null
}
```

---

## Response Endpoints

### Create Response

**Endpoint:** `POST /responses/`

**Request Body:**
```json
{
  "session_id": 1 (required),
  "candidate_id": 1 (required),
  "question_id": 1 (required),
  "response_text": "string (optional)",
  "response_audio_path": "string (optional)",
  "response_type": "text|voice (default: text)"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Response created successfully",
  "data": {
    "id": 1,
    "session_id": 1,
    "candidate_id": 1,
    "question_id": 1,
    "response_text": "I have 5 years of experience...",
    "response_audio_path": null,
    "response_type": "text",
    "submitted_at": "2024-01-01T00:00:00"
  }
}
```

### Get Response

**Endpoint:** `GET /responses/{response_id}`

**Response:** Same as Create Response response

### Get All Responses

**Endpoint:** `GET /responses/`

**Query Parameters:**
- `page`: integer (default: 1)
- `page_size`: integer (default: 10, max: 100)

**Response:**
```json
{
  "success": true,
  "message": "Responses retrieved successfully",
  "data": [...],
  "total": 1,
  "page": 1,
  "page_size": 10
}
```

### Get Responses by Session

**Endpoint:** `GET /responses/session/{session_id}`

**Response:**
```json
{
  "success": true,
  "message": "Responses for session 1 retrieved successfully",
  "data": [...],
  "total": 1
}
```

### Get Responses by Candidate

**Endpoint:** `GET /responses/candidate/{candidate_id}`

**Query Parameters:**
- `page`: integer (default: 1)
- `page_size`: integer (default: 10, max: 100)

**Response:** Same as Get All Responses

### Get Latest Response

**Endpoint:** `GET /responses/candidate/{candidate_id}/latest`

**Response:** Same as Get Response response

### Update Response

**Endpoint:** `PUT /responses/{response_id}`

**Request Body:**
```json
{
  "response_text": "string (optional)",
  "response_audio_path": "string (optional)",
  "response_type": "text|voice (optional)"
}
```

**Response:** Same as Get Response response

### Delete Response

**Endpoint:** `DELETE /responses/{response_id}`

**Response:**
```json
{
  "success": true,
  "message": "Response deleted successfully",
  "data": null
}
```

### Create Voice Response

**Endpoint:** `POST /responses/voice`

**Request:**
- `audio_file`: multipart/form-data (required)
- `session_id`: query parameter (required)
- `candidate_id`: query parameter (required)
- `question_id`: query parameter (required)

**Response:** Same as Create Response response

---

## Feedback Endpoints

### Create Feedback

**Endpoint:** `POST /feedback/`

**Request Body:**
```json
{
  "response_id": 1 (required),
  "session_id": 1 (required),
  "candidate_id": 1 (required),
  "question_id": 1 (required),
  "relevance_score": 85.5,
  "clarity_score": 75.0,
  "structure_score": 80.0,
  "completeness_score": 70.0,
  "communication_score": 85.0,
  "overall_score": 79.1,
  "strengths": ["Clear articulation", "Relevant experience"],
  "weaknesses": ["Could be more concise"],
  "improvement_suggestions": ["Use STAR method"],
  "star_analysis": "Good situation description...",
  "content_analysis": "Response addresses the question well...",
  "communication_analysis": "Clear and professional tone...",
  "improved_response": "I have 5 years of experience...",
  "follow_up_questions": ["Can you elaborate?"],
  "agent_feedback": {}
}
```

**Response:**
```json
{
  "success": true,
  "message": "Feedback created successfully",
  "data": {...}
}
```

### Get Feedback

**Endpoint:** `GET /feedback/{feedback_id}`

**Response:** Same as Create Feedback response

### Get Feedback by Response

**Endpoint:** `GET /feedback/response/{response_id}`

**Response:** Same as Get Feedback response

### Get Feedback by Session

**Endpoint:** `GET /feedback/session/{session_id}`

**Response:**
```json
{
  "success": true,
  "message": "Feedback for session 1 retrieved successfully",
  "data": [...],
  "total": 1
}
```

### Get Feedback by Candidate

**Endpoint:** `GET /feedback/candidate/{candidate_id}`

**Query Parameters:**
- `page`: integer (default: 1)
- `page_size`: integer (default: 10, max: 100)

**Response:** Same as Get Feedback by Session

### Get Average Scores

**Endpoint:** `GET /feedback/candidate/{candidate_id}/average-scores`

**Response:**
```json
{
  "success": true,
  "message": "Average scores retrieved successfully",
  "data": {
    "relevance": 85.5,
    "clarity": 75.0,
    "structure": 80.0,
    "completeness": 70.0,
    "communication": 85.0,
    "overall": 79.1
  }
}
```

### Analyze Response (Multi-Agent)

**Endpoint:** `POST /feedback/analyze`

**Query Parameters:**
- `candidate_id`: integer (required)
- `question_id`: integer (required)
- `response_text`: string (required)
- `session_id`: integer (optional)
- `response_type`: string (default: text)

**Response:**
```json
{
  "success": true,
  "message": "Response analyzed successfully using multi-agent system",
  "feedback": {
    "overall_score": 82.5,
    "performance_summary": "Good response with room for improvement",
    "agent_feedback_summary": {
      "communication": {
        "score": 85.0,
        "strengths": ["Clear articulation"],
        "weaknesses": ["Could be more concise"],
        "suggestions": ["Use shorter sentences"]
      },
      "content": {
        "score": 80.0,
        "strengths": ["Relevant experience"],
        "weaknesses": ["Missing some details"],
        "suggestions": ["Add more specifics"]
      },
      "star": {
        "score": 75.0,
        "strengths": ["Good situation"],
        "weaknesses": ["Weak action"],
        "suggestions": ["Describe actions more"]
      }
    },
    "recurring_patterns": [],
    "personalized_recommendations": [
      {
        "area": "communication",
        "action": "Practice concise communication",
        "priority": "medium"
      }
    ],
    "follow_up_questions": ["Can you elaborate?"],
    "improvement_plan": {
      "short_term": ["Practice daily"],
      "medium_term": ["Review feedback"],
      "long_term": ["Build experience"]
    },
    "improved_response_example": "I have 5 years of experience...",
    "motivational_feedback": "Good job! Keep practicing."
  },
  "agent_analysis": {
    "communication_agent": {...},
    "content_agent": {...},
    "star_agent": {...},
    "coach_agent": {...}
  },
  "multi_agent_summary": {
    "overall_score": 82.5,
    "performance_summary": "Good response with room for improvement",
    "improvement_plan": {...},
    "follow_up_questions": ["Can you elaborate?"]
  }
}
```

### Quick Analyze Response

**Endpoint:** `POST /feedback/quick-analyze`

**Query Parameters:**
- `response_text`: string (required)
- `question`: string (required)

**Response:** Same as Get Feedback response

### Update Feedback

**Endpoint:** `PUT /feedback/{feedback_id}`

**Request Body:** Same as Create Feedback (all fields optional)

**Response:** Same as Get Feedback response

### Delete Feedback

**Endpoint:** `DELETE /feedback/{feedback_id}`

**Response:**
```json
{
  "success": true,
  "message": "Feedback deleted successfully",
  "data": null
}
```

### Get Feedback Context

**Endpoint:** `GET /feedback/{feedback_id}/context`

**Response:**
```json
{
  "success": true,
  "message": "Feedback context retrieved successfully",
  "data": {
    "feedback": {...},
    "response": {...},
    "question": {...},
    "candidate": {...}
  }
}
```

---

## Agent Endpoints

### Get Agent Status

**Endpoint:** `GET /agents/status`

**Response:**
```json
{
  "success": true,
  "message": "Agent status retrieved successfully",
  "data": {
    "agents": {
      "question_agent": {"status": "ready", "type": "question_selection"},
      "communication_agent": {"status": "ready", "type": "communication_analysis"},
      "content_agent": {"status": "ready", "type": "content_evaluation"},
      "star_agent": {"status": "ready", "type": "star_analysis"},
      "coach_agent": {"status": "ready", "type": "coaching_consolidation"}
    },
    "all_ready": true,
    "timestamp": "2024-01-01T00:00:00"
  }
}
```

### Initialize Agents

**Endpoint:** `POST /agents/initialize`

**Response:**
```json
{
  "success": true,
  "message": "Agents initialized successfully",
  "data": {"all_initialized": true}
}
```

### Start Practice Session

**Endpoint:** `POST /agents/practice/start`

**Query Parameters:**
- `candidate_id`: integer (required)
- `target_role`: string (optional)
- `competency`: string (optional)
- `difficulty`: string (default: medium)

**Response:**
```json
{
  "success": true,
  "message": "Practice session started successfully",
  "data": {
    "question": {
      "id": 1,
      "text": "Tell me about a challenging project...",
      "role": "Software Engineer",
      "competency": "Problem Solving",
      "difficulty": "medium",
      "question_type": "behavioral"
    },
    "session": {
      "candidate_id": 1,
      "question_id": 1,
      "session_type": "practice",
      "status": "in_progress"
    }
  }
}
```

### Analyze Practice Response

**Endpoint:** `POST /agents/practice/analyze`

**Query Parameters:**
- `candidate_id`: integer (required)
- `question_id`: integer (required)
- `response_text`: string (required)
- `session_id`: integer (optional)
- `response_type`: string (default: text)

**Response:**
```json
{
  "success": true,
  "message": "Response analyzed successfully with multi-agent system",
  "data": {
    "question": {...},
    "feedback": {...},
    "response_analysis": {...},
    "agent_results": {...},
    "improvement_plan": {...},
    "follow_up_questions": [...],
    "metadata": {...}
  }
}
```

### Get Follow-up Question

**Endpoint:** `POST /agents/follow-up`

**Query Parameters:**
- `candidate_id`: integer (required)
- `previous_question_id`: integer (required)
- `previous_response`: string (required)

**Response:**
```json
{
  "success": true,
  "message": "Follow-up question generated successfully",
  "data": {
    "question": {
      "text": "Can you elaborate on that?",
      "type": "follow_up",
      "original_question_id": 1
    },
    "metadata": {...}
  }
}
```

### Generate Improvement Plan

**Endpoint:** `POST /agents/improvement-plan`

**Query Parameters:**
- `candidate_id`: integer (required)
- `num_sessions`: integer (default: 5)

**Response:**
```json
{
  "success": true,
  "message": "Improvement plan generated successfully",
  "data": {
    "candidate_id": 1,
    "target_role": "Software Engineer",
    "average_scores": {
      "relevance": 85.5,
      "clarity": 75.0,
      "structure": 80.0,
      "completeness": 70.0,
      "communication": 85.0,
      "overall": 79.1
    },
    "common_strengths": ["Clear communication"],
    "common_weaknesses": ["Needs more detail"],
    "focus_areas": ["Structure", "Completeness"],
    "recommended_actions": [
      "Practice STAR method daily",
      "Record and review responses"
    ],
    "estimated_improvement_timeline": "4-6 weeks"
  },
  "metadata": {...}
}
```

### Analyze Communication

**Endpoint:** `GET /agents/communication/analyze`

**Query Parameters:**
- `response_text`: string (required)
- `question`: string (required)

**Response:**
```json
{
  "success": true,
  "message": "Communication analysis completed",
  "data": {
    "scores": {
      "clarity_score": 85.0,
      "structure_score": 80.0,
      "conciseness_score": 75.0,
      "tone_score": 90.0,
      "overall_communication_score": 82.5
    },
    "analysis": {...},
    "text_metrics": {
      "word_count": 150,
      "sentence_count": 10,
      "avg_sentence_length": 15.0,
      "character_count": 800
    },
    "strengths": [...],
    "weaknesses": [...],
    "suggestions": [...]
  }
}
```

### Analyze Content

**Endpoint:** `GET /agents/content/analyze`

**Query Parameters:**
- `response_text`: string (required)
- `question`: string (required)

**Response:**
```json
{
  "success": true,
  "message": "Content analysis completed",
  "data": {
    "scores": {
      "relevance_score": 90.0,
      "completeness_score": 85.0,
      "knowledge_score": 88.0,
      "experience_score": 82.0,
      "overall_content_score": 86.25
    },
    "analysis": {...},
    "addresses_question": true,
    "missing_elements": [...],
    "strengths": [...],
    "weaknesses": [...],
    "suggestions": [...],
    "text_comparison": {...}
  }
}
```

### Analyze STAR

**Endpoint:** `GET /agents/star/analyze`

**Query Parameters:**
- `response_text`: string (required)
- `question`: string (required)

**Response:**
```json
{
  "success": true,
  "message": "STAR analysis completed",
  "data": {
    "scores": {
      "situation_score": 80.0,
      "task_score": 85.0,
      "action_score": 70.0,
      "result_score": 75.0,
      "overall_star_score": 77.5
    },
    "uses_star_structure": true,
    "missing_components": ["action"],
    "star_breakdown": {
      "situation": {"text": "...", "detected": true, "score": 80.0},
      "task": {"text": "...", "detected": true, "score": 85.0},
      "action": {"text": "...", "detected": false, "score": 0.0},
      "result": {"text": "...", "detected": true, "score": 75.0}
    },
    "strengths": [...],
    "weaknesses": [...],
    "suggestions": [...],
    "detailed_analysis": "..."
  }
}
```

### Generate STAR Example

**Endpoint:** `GET /agents/star/example`

**Query Parameters:**
- `question`: string (required)

**Response:**
```json
{
  "success": true,
  "message": "STAR example generated",
  "data": {
    "response": "Situation: In my previous role... Task: My responsibility was... Action: I implemented... Result: This led to..."
  }
}
```

---

## Progress Endpoints

### Create Progress

**Endpoint:** `POST /progress/`

**Request Body:**
```json
{
  "candidate_id": 1 (required),
  "session_id": 1 (optional),
  "competency": "string (required)",
  "score": 85.5 (required),
  "area": "string (required)",
  "baseline_score": 70.0,
  "current_score": 85.5,
  "improvement_percentage": 22.14
}
```

**Response:**
```json
{
  "success": true,
  "message": "Progress entry created successfully",
  "data": {...}
}
```

### Get Progress

**Endpoint:** `GET /progress/{progress_id}`

**Response:** Same as Create Progress response

### Get Progress by Candidate

**Endpoint:** `GET /progress/candidate/{candidate_id}`

**Query Parameters:**
- `page`: integer (default: 1)
- `page_size`: integer (default: 10, max: 100)

**Response:**
```json
{
  "success": true,
  "message": "Progress for candidate 1 retrieved successfully",
  "data": [...],
  "total": 1,
  "page": 1,
  "page_size": 10
}
```

### Get Progress Summary

**Endpoint:** `GET /progress/candidate/{candidate_id}/summary`

**Response:**
```json
{
  "success": true,
  "message": "Progress summary retrieved successfully",
  "data": {
    "overall": {
      "average_score": 82.5,
      "total_sessions": 10,
      "improvement_trend": "improving"
    },
    "by_competency": {
      "Communication": {"scores": [80, 85, 90], "average": 85, "count": 3},
      "Problem Solving": {"scores": [75, 80, 85], "average": 80, "count": 3}
    },
    "by_area": {
      "relevance": {"scores": [85, 90, 95], "average": 90, "count": 3},
      "clarity": {"scores": [75, 80, 85], "average": 80, "count": 3}
    },
    "recent_trend": [
      {"session_id": 1, "score": 80, "date": "2024-01-01"},
      {"session_id": 2, "score": 85, "date": "2024-01-02"}
    ]
  }
}
```

### Get Progress by Competency

**Endpoint:** `GET /progress/candidate/{candidate_id}/competency/{competency}`

**Response:**
```json
{
  "success": true,
  "message": "Progress for competency 'Communication' retrieved successfully",
  "data": [...],
  "total": 1
}
```

### Get Improvement Areas

**Endpoint:** `GET /progress/candidate/{candidate_id}/improvement-areas`

**Query Parameters:**
- `threshold`: float (default: 70.0)

**Response:**
```json
{
  "success": true,
  "message": "Improvement areas identified successfully",
  "data": [
    {
      "type": "area",
      "name": "Structure",
      "current_score": 65.0,
      "deficit": 5.0
    },
    {
      "type": "competency",
      "name": "Technical",
      "current_score": 68.0,
      "deficit": 2.0
    }
  ],
  "threshold": 70.0
}
```

### Get Latest Progress

**Endpoint:** `GET /progress/candidate/{candidate_id}/competency/{competency}/area/{area}`

**Response:** Same as Get Progress response

### Update Progress Scores

**Endpoint:** `PUT /progress/{progress_id}/update`

**Query Parameters:**
- `current_score`: float (required)
- `improvement_percentage`: float (required)

**Response:** Same as Get Progress response

---

## Voice Endpoints

### Transcribe Audio

**Endpoint:** `POST /voice/transcribe`

**Request:**
- `audio_file`: multipart/form-data (required)

**Response:**
```json
{
  "success": true,
  "message": "Audio transcribed successfully",
  "data": {
    "transcription": "This is the transcribed text...",
    "audio_path": "/uploads/audio/file.wav",
    "filename": "file.wav"
  }
}
```

### Upload Voice Response

**Endpoint:** `POST /voice/upload`

**Request:**
- `audio_file`: multipart/form-data (required)
- `session_id`: query parameter (required)
- `candidate_id`: query parameter (required)
- `question_id`: query parameter (required)

**Response:**
```json
{
  "success": true,
  "message": "Voice response uploaded and transcribed successfully",
  "data": {
    "response_id": 1,
    "transcription": "This is the transcribed text...",
    "audio_path": "/uploads/audio/file.wav",
    "filename": "file.wav",
    "session_id": 1,
    "candidate_id": 1,
    "question_id": 1
  }
}
```

### Get Audio Duration

**Endpoint:** `GET /voice/duration/{audio_path}`

**Response:**
```json
{
  "success": true,
  "message": "Audio duration retrieved successfully",
  "data": {
    "path": "/uploads/audio/file.wav",
    "duration_seconds": 30.5
  }
}
```

### Convert Audio Format

**Endpoint:** `POST /voice/convert`

**Request:**
- `audio_file`: multipart/form-data (required)
- `output_format`: query parameter (default: wav)

**Response:**
```json
{
  "success": true,
  "message": "Audio converted successfully",
  "data": {
    "original_filename": "file.mp3",
    "converted_format": "wav",
    "converted_data": "base64-encoded-audio-data"
  }
}
```

---

## Error Handling

All endpoints may return error responses in the following format:

```json
{
  "success": false,
  "message": "Error message",
  "data": null
}
```

### Common Error Codes

| Status Code | Description | Example Message |
|-------------|-------------|----------------|
| 400 | Bad Request | "Invalid input data" |
| 401 | Unauthorized | "Authentication required" |
| 403 | Forbidden | "Admin access required" |
| 404 | Not Found | "Resource not found" |
| 409 | Conflict | "Username already exists" |
| 422 | Validation Error | "Field 'email' is required" |
| 429 | Rate Limit | "Too many requests" |
| 500 | Server Error | "Internal server error" |

---

## Rate Limiting

Currently not implemented, but can be added with the following limits:

- **Anonymous users**: 10 requests/minute
- **Authenticated users**: 100 requests/minute
- **Admin users**: 1000 requests/minute

---

## Versioning

The API uses URL path versioning. All endpoints are currently at version 1:

```
/api/v1/...
```

Future versions will be available at:
```
/api/v2/...
```

---

## Changelog

### Version 1.0.0 (Current)
- Initial release
- All core endpoints implemented
- Multi-agent system integrated
- Authentication and authorization
- Progress tracking

### Version 1.1.0 (Planned)
- Rate limiting
- Enhanced error handling
- More detailed analytics
- Export/import functionality

### Version 2.0.0 (Future)
- Video interview support
- Real-time collaboration
- Advanced analytics dashboard
- Machine learning improvements
