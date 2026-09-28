"""
Seed Data Script for Interview Coach
Populates the database with sample questions and data for testing
"""

import asyncio
import json
from database import get_db_dict
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Sample questions data
SAMPLE_QUESTIONS = [
    {
        "question_text": "Tell me about yourself.",
        "role": "Software Engineer",
        "competency": "Communication",
        "difficulty": "easy",
        "question_type": "behavioral",
        "expected_competency": "Clear and concise self-introduction",
        "evaluation_criteria": json.dumps(["Clarity", "Relevance", "Structure"]),
        "category": "general",
        "is_active": True
    },
    {
        "question_text": "Why are you interested in this role?",
        "role": "Software Engineer",
        "competency": "Motivation",
        "difficulty": "easy",
        "question_type": "behavioral",
        "expected_competency": "Demonstrates genuine interest and alignment with role",
        "evaluation_criteria": json.dumps(["Relevance", "Enthusiasm", "Alignment"]),
        "category": "general",
        "is_active": True
    },
    {
        "question_text": "Describe a challenging project you worked on.",
        "role": "Software Engineer",
        "competency": "Problem Solving",
        "difficulty": "medium",
        "question_type": "behavioral",
        "expected_competency": "STAR method demonstration with clear outcomes",
        "evaluation_criteria": json.dumps(["Situation", "Task", "Action", "Result", "Impact"]),
        "category": "technical",
        "is_active": True
    },
    {
        "question_text": "How would you handle a difficult customer or stakeholder?",
        "role": "Software Engineer",
        "competency": "Conflict Resolution",
        "difficulty": "medium",
        "question_type": "situational",
        "expected_competency": "Professional conflict resolution approach",
        "evaluation_criteria": json.dumps(["Empathy", "Professionalism", "Solution Focus", "Communication"]),
        "category": "behavioral",
        "is_active": True
    },
    {
        "question_text": "Explain this technical concept in simple terms.",
        "role": "Software Engineer",
        "competency": "Technical Communication",
        "difficulty": "hard",
        "question_type": "technical",
        "expected_competency": "Ability to simplify complex concepts",
        "evaluation_criteria": json.dumps(["Clarity", "Simplicity", "Accuracy", "Engagement"]),
        "category": "technical",
        "is_active": True
    },
    {
        "question_text": "What are your strengths and weaknesses?",
        "role": "Software Engineer",
        "competency": "Self-Awareness",
        "difficulty": "easy",
        "question_type": "behavioral",
        "expected_competency": "Honest self-assessment with growth mindset",
        "evaluation_criteria": json.dumps(["Honesty", "Relevance", "Growth Mindset", "Balance"]),
        "category": "general",
        "is_active": True
    },
    {
        "question_text": "Where do you see yourself in 5 years?",
        "role": "Software Engineer",
        "competency": "Career Vision",
        "difficulty": "easy",
        "question_type": "behavioral",
        "expected_competency": "Realistic career goals aligned with company growth",
        "evaluation_criteria": json.dumps(["Realism", "Alignment", "Ambition", "Clarity"]),
        "category": "general",
        "is_active": True
    },
    {
        "question_text": "How do you handle tight deadlines?",
        "role": "Software Engineer",
        "competency": "Time Management",
        "difficulty": "medium",
        "question_type": "situational",
        "expected_competency": "Effective prioritization and stress management",
        "evaluation_criteria": json.dumps(["Prioritization", "Time Management", "Stress Management", "Quality Maintenance"]),
        "category": "behavioral",
        "is_active": True
    },
    {
        "question_text": "Describe a time you made a mistake and how you handled it.",
        "role": "Software Engineer",
        "competency": "Accountability",
        "difficulty": "medium",
        "question_type": "behavioral",
        "expected_competency": "Takes ownership and demonstrates learning",
        "evaluation_criteria": json.dumps(["Ownership", "Learning", "Improvement", "Honesty"]),
        "category": "behavioral",
        "is_active": True
    },
    {
        "question_text": "How do you stay updated with new technologies?",
        "role": "Software Engineer",
        "competency": "Continuous Learning",
        "difficulty": "easy",
        "question_type": "behavioral",
        "expected_competency": "Proactive learning and application of new skills",
        "evaluation_criteria": json.dumps(["Proactivity", "Application", "Resources", "Sharing"]),
        "category": "technical",
        "is_active": True
    }
]


async def seed_database():
    """Seed the database with sample data"""
    print("Seeding database...")
    
    # Initialize database
    from database import init_db
    await init_db()
    
    conn = await get_db_dict()
    cursor = conn.cursor()
    
    try:
        # Clear existing data
        cursor.execute("DELETE FROM users")
        cursor.execute("DELETE FROM questions")
        cursor.execute("DELETE FROM candidates")
        cursor.execute("DELETE FROM sessions")
        cursor.execute("DELETE FROM responses")
        cursor.execute("DELETE FROM feedback")
        cursor.execute("DELETE FROM progress")
        cursor.execute("DELETE FROM agent_analysis")
        cursor.execute("DELETE FROM improvement_plans")
        cursor.execute("DELETE FROM api_keys")
        
        conn.commit()
        print("  Cleared existing data")
        
        # Insert sample user
        hashed_password = pwd_context.hash("password")
        cursor.execute("""
            INSERT INTO users (username, email, hashed_password, full_name, is_active, is_admin)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ("testuser", "test@example.com", hashed_password, "Test User", 1, 0))
        conn.commit()
        print("  Inserted sample user")
        
        # Insert sample questions
        for question in SAMPLE_QUESTIONS:
            cursor.execute("""
                INSERT INTO questions (question_text, role, competency, difficulty, question_type, expected_competency, evaluation_criteria, category, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                question["question_text"],
                question["role"],
                question["competency"],
                question["difficulty"],
                question["question_type"],
                question["expected_competency"],
                question["evaluation_criteria"],
                question["category"],
                question["is_active"]
            ))
        conn.commit()
        print(f"  Inserted {len(SAMPLE_QUESTIONS)} sample questions")
        
        # Verify data
        cursor.execute("SELECT COUNT(*) FROM users")
        user_row = cursor.fetchone()
        user_count = user_row['COUNT(*)'] if isinstance(user_row, dict) else user_row[0]
        cursor.execute("SELECT COUNT(*) FROM questions")
        question_row = cursor.fetchone()
        question_count = question_row['COUNT(*)'] if isinstance(question_row, dict) else question_row[0]
        
        print(f"\nDatabase seeded successfully!")
        print(f"  Users: {user_count}")
        print(f"  Questions: {question_count}")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    asyncio.run(seed_database())
