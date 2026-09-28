"""
Test script for Interview Coach Backend
"""

import sys
import os

# Add the backend directory to the path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.dirname(backend_dir))

# Now import the app
from backend.main import app
from fastapi.testclient import TestClient

# Create test client
client = TestClient(app)

# Test endpoints
print("=== Testing Interview Coach Backend ===\n")

# Test 1: Root endpoint
print("1. Testing Root Endpoint (/api/)")
response = client.get("/api/")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")
print()

# Test 2: Health check
print("2. Testing Health Check (/api/health)")
response = client.get("/api/health")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")
print()

# Test 3: Question statistics
print("3. Testing Question Statistics (/api/questions/stats)")
response = client.get("/api/questions/stats")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print(f"   Response: {response.json()}")
else:
    print(f"   Error: {response.text}")
print()

# Test 4: Register user
print("4. Testing User Registration (/api/auth/register)")
response = client.post("/api/auth/register", json={
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "testpass123"
})
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")
print()

# Test 5: Login
print("5. Testing User Login (/api/auth/token)")
response = client.post("/api/auth/token", data={
    "username": "testuser",
    "password": "testpass123"
})
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")
print()

# Test 6: Create candidate
print("6. Testing Candidate Creation (/api/candidates/)")
# Get token first
login_response = client.post("/api/auth/token", data={
    "username": "testuser",
    "password": "testpass123"
})
token = login_response.json().get("access_token")

if token:
    response = client.post("/api/candidates/", json={
        "user_id": "testuser",
        "name": "Test Candidate",
        "email": "test@example.com",
        "target_role": "Software Engineer",
        "experience_years": 5,
        "skills": ["Python", "FastAPI"],
        "competencies": ["Problem Solving"]
    }, headers={"Authorization": f"Bearer {token}"})
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
else:
    print("   Skipped: No token received")
print()

# Test 7: Get random question
print("7. Testing Random Question (/api/questions/random)")
response = client.get("/api/questions/random")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")
print()

# Test 8: Multi-agent analysis
print("8. Testing Multi-Agent Analysis (/api/feedback/quick-analyze)")
response = client.post("/api/feedback/quick-analyze?response_text=I have 5 years of experience in software development and have worked on various projects.&question=Tell me about yourself")
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   Overall Score: {data.get('data', {}).get('overall_score', 'N/A')}")
    print(f"   Success: {data.get('success', False)}")
else:
    print(f"   Error: {response.text[:200]}")
print()

print("=== All Tests Completed ===")
