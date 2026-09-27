"""
Interview Question Bank
Manages a curated set of interview questions organized by role, competency, difficulty, and type.
Includes 600+ real-world interview questions loaded from backend/data/interview_questions.csv.
"""
import os
import random
import uuid
import pandas as pd
from typing import Optional
from models import InterviewQuestion, CandidateProfile
from llm_client import llm_client, extract_json

# ──────────────────────────────────────────────────────────────
# Built-in General & Management Question Bank
# ──────────────────────────────────────────────────────────────
GENERAL_QUESTIONS: list[dict] = [
    {"question": "Tell me about yourself.", "role": "General", "competency": "Communication", "difficulty": "entry", "question_type": "behavioral", "expected_competencies": ["self-awareness", "communication", "conciseness"], "hints": ["Keep it to 90 seconds", "Highlight relevant background"]},
    {"question": "Why are you interested in this role?", "role": "General", "competency": "Motivation", "difficulty": "entry", "question_type": "motivational", "expected_competencies": ["research", "enthusiasm", "alignment"], "hints": ["Connect your career goals to the company's mission"]},
    {"question": "Describe a challenging project you worked on.", "role": "General", "competency": "Problem Solving", "difficulty": "intermediate", "question_type": "behavioral", "expected_competencies": ["problem-solving", "resilience", "teamwork"], "hints": ["Use the STAR method: Situation, Task, Action, Result"]},
    {"question": "How would you handle a difficult customer or stakeholder?", "role": "General", "competency": "Conflict Resolution", "difficulty": "intermediate", "question_type": "situational", "expected_competencies": ["empathy", "communication", "negotiation"], "hints": ["Focus on active listening and finding win-win outcomes"]},
    {"question": "Tell me about a time you failed and what you learned from it.", "role": "General", "competency": "Self-Awareness", "difficulty": "intermediate", "question_type": "behavioral", "expected_competencies": ["self-awareness", "growth-mindset", "accountability"], "hints": ["Own the outcome and explain your key takeaways"]},
    {"question": "Describe a situation where you had to lead a team through ambiguity.", "role": "General", "competency": "Leadership", "difficulty": "advanced", "question_type": "behavioral", "expected_competencies": ["leadership", "decision-making", "communication"], "hints": ["Show how you established clarity and rallied the team"]},
    {"question": "How do you prioritize competing deadlines?", "role": "General", "competency": "Time Management", "difficulty": "intermediate", "question_type": "situational", "expected_competencies": ["prioritization", "organization", "communication"], "hints": ["Mention frameworks like Eisenhower matrix or agile sprints"]},

    # Data Scientist
    {"question": "How would you approach a new machine learning problem from scratch?", "role": "Data Scientist", "competency": "Problem Solving", "difficulty": "intermediate", "question_type": "technical", "expected_competencies": ["methodology", "data-understanding", "model-selection"], "hints": ["Start with exploratory data analysis and baseline metrics"]},
    {"question": "Explain overfitting and how you prevent it.", "role": "Data Scientist", "competency": "Technical Knowledge", "difficulty": "intermediate", "question_type": "technical", "expected_competencies": ["ML-fundamentals", "regularization", "validation"], "hints": ["Discuss cross-validation, L1/L2 regularization, dropout, and data augmentation"]},
    {"question": "Describe a project where your analysis led to a significant business decision.", "role": "Data Scientist", "competency": "Business Impact", "difficulty": "advanced", "question_type": "behavioral", "expected_competencies": ["business-acumen", "storytelling", "impact-measurement"], "hints": ["Quantify the business outcome with measurable KPIs"]},

    # Product Manager
    {"question": "How do you prioritize features for a product roadmap?", "role": "Product Manager", "competency": "Prioritization", "difficulty": "intermediate", "question_type": "situational", "expected_competencies": ["frameworks", "stakeholder-management", "data-driven"], "hints": ["Explain RICE, MoSCoW, or Value vs Effort matrices"]},
    {"question": "Tell me about a product you launched from ideation to release.", "role": "Product Manager", "competency": "Execution", "difficulty": "advanced", "question_type": "behavioral", "expected_competencies": ["planning", "execution", "iteration"], "hints": ["Structure around customer research, MVP, feedback loops, and metrics"]},

    # DevOps Engineer
    {"question": "Explain how you design a resilient CI/CD pipeline with zero-downtime deployment.", "role": "DevOps Engineer", "competency": "CI/CD & Infrastructure", "difficulty": "advanced", "question_type": "technical", "expected_competencies": ["blue-green deployment", "canary releases", "automated testing"], "hints": ["Discuss health checks, rollbacks, and blue-green or canary deployments"]},
]

LEVEL_TO_DIFFICULTY = {
    "Easy": "entry",
    "Medium": "intermediate",
    "Hard": "advanced",
}

DIFFICULTY_TO_LEVEL = {
    "entry": "Easy",
    "intermediate": "Medium",
    "advanced": "Hard",
    "expert": "Hard",
}

# Role to Technology / Language Mapping
ROLE_TECH_MAPPING: dict[str, list[str]] = {
    "Java Developer": ["Java"],
    "PHP Developer": ["PHP"],
    "Magento Developer": ["Magento", "PHP"],
    "Software Engineer": ["Java"],
    "Backend Developer": ["Java", "PHP"],
    "Full Stack Developer": ["Java", "PHP"],
    "Web Developer": ["PHP", "Magento"],
}


class QuestionBankManager:
    """Manages combined CSV question bank and dynamic generation."""

    def __init__(self):
        self.csv_questions: list[InterviewQuestion] = []
        self._load_csv()

    def _load_csv(self):
        """Load questions from interview_questions.csv."""
        csv_path = os.path.join(os.path.dirname(__file__), "data", "interview_questions.csv")
        if not os.path.exists(csv_path):
            print(f"[QuestionBank] CSV file not found at {csv_path}")
            return

        try:
            df = pd.read_csv(csv_path)
            questions_list = []
            for _, row in df.iterrows():
                lang = str(row.get("language", "")).strip()
                lvl = str(row.get("level", "Medium")).strip()
                q_text = str(row.get("question", "")).strip()
                ans_text = str(row.get("answer", "") or "").strip()
                qid = str(row.get("qid", str(uuid.uuid4())[:6]))

                if not q_text:
                    continue

                diff = LEVEL_TO_DIFFICULTY.get(lvl, "intermediate")
                role_label = f"{lang} Developer" if lang in ["Java", "PHP", "Magento"] else "Software Engineer"

                iq = InterviewQuestion(
                    id=f"csv-{qid}",
                    question=q_text,
                    role=role_label,
                    competency=f"{lang} Core",
                    difficulty=diff,
                    question_type="technical",
                    expected_competencies=[lang, "Core Concepts", "Problem Solving"],
                    hints=[f"Explain the underlying mechanism and provide practical {lang} examples."],
                    follow_up_questions=[
                        f"How does this behave in high-concurrency or enterprise {lang} applications?",
                        f"What are the performance implications or trade-offs?"
                    ],
                    reference_answer=ans_text,
                    language=lang,
                    source="interview_questions.csv",
                )
                questions_list.append(iq)

            self.csv_questions = questions_list
            print(f"[QuestionBank] Successfully loaded {len(self.csv_questions)} questions from CSV")
        except Exception as e:
            print(f"[QuestionBank] Failed to load CSV questions: {e}")

    def get_csv_questions_for_role(
        self,
        role: str,
        difficulty: Optional[str] = None,
        skills: Optional[list[str]] = None,
    ) -> list[InterviewQuestion]:
        """Filter CSV questions by target role and difficulty."""
        # Find matching languages for this role
        target_techs = ROLE_TECH_MAPPING.get(role, [])
        if not target_techs:
            # Check if role matches directly (e.g. "Java", "PHP", "Magento")
            for tech in ["Java", "PHP", "Magento"]:
                if tech.lower() in role.lower():
                    target_techs.append(tech)

        # Check candidate profile skills
        if skills:
            for s in skills:
                for tech in ["Java", "PHP", "Magento"]:
                    if tech.lower() in s.lower() and tech not in target_techs:
                        target_techs.append(tech)

        if not target_techs:
            # Fallback for general software engineer
            if "software" in role.lower() or "developer" in role.lower() or "engineer" in role.lower():
                target_techs = ["Java"]
            else:
                return []

        # Filter by technology
        matched = [q for q in self.csv_questions if q.language in target_techs]

        # Filter by difficulty if provided
        if difficulty:
            diff_matched = [q for q in matched if q.difficulty == difficulty]
            if diff_matched:
                return diff_matched

        return matched

    def get_all_questions(
        self,
        role: Optional[str] = None,
        competency: Optional[str] = None,
        difficulty: Optional[str] = None,
        question_type: Optional[str] = None,
    ) -> list[InterviewQuestion]:
        """Get combined questions from CSV and general bank."""
        results = []

        # CSV questions
        if role:
            csv_matches = self.get_csv_questions_for_role(role, difficulty=difficulty)
            results.extend(csv_matches)
        else:
            results.extend(self.csv_questions)

        # General questions
        general_matches = GENERAL_QUESTIONS
        if role:
            general_matches = [
                q for q in general_matches
                if q["role"].lower() == role.lower() or q["role"] == "General"
            ]
        if difficulty:
            general_matches = [q for q in general_matches if q["difficulty"] == difficulty]

        for g in general_matches:
            results.append(
                InterviewQuestion(
                    id=str(uuid.uuid4())[:8],
                    source="general_bank",
                    **g
                )
            )

        # Apply competency and question_type filters
        if competency:
            results = [q for q in results if competency.lower() in q.competency.lower()]
        if question_type:
            results = [q for q in results if q.question_type == question_type]

        return results


# Global singleton
question_manager = QuestionBankManager()


def get_questions(
    role: Optional[str] = None,
    competency: Optional[str] = None,
    difficulty: Optional[str] = None,
    question_type: Optional[str] = None,
) -> list[InterviewQuestion]:
    """Filter and return questions from the bank."""
    return question_manager.get_all_questions(
        role=role,
        competency=competency,
        difficulty=difficulty,
        question_type=question_type,
    )


def get_random_question(
    role: Optional[str] = None,
    difficulty: Optional[str] = None,
    candidate_profile: Optional[CandidateProfile] = None,
) -> InterviewQuestion:
    """Get a random question based on role, prioritizing role-specific CSV questions."""
    skills = candidate_profile.skills if candidate_profile else None
    role_name = role or (candidate_profile.target_role if candidate_profile else "Software Engineer")

    # 1. Try role-matched CSV questions first
    csv_questions = question_manager.get_csv_questions_for_role(
        role=role_name,
        difficulty=difficulty,
        skills=skills,
    )
    if csv_questions:
        return random.choice(csv_questions)

    # 2. Try general bank questions
    all_q = get_questions(role=role_name, difficulty=difficulty)
    if all_q:
        return random.choice(all_q)

    # 3. Ultimate fallback
    return InterviewQuestion(
        id="default-1",
        question=f"Describe your background and most impactful experience as a {role_name}.",
        role=role_name,
        competency="Experience",
        difficulty=difficulty or "intermediate",
        question_type="behavioral",
        expected_competencies=["communication", "domain-knowledge"],
        hints=["Use the STAR method", "Highlight measurable accomplishments"],
        source="default",
    )


async def generate_question_with_ai(
    role: str,
    competency: str = "",
    difficulty: str = "intermediate",
    candidate_profile: Optional[CandidateProfile] = None,
    source_preference: str = "auto",
) -> InterviewQuestion:
    """
    Get or generate an interview question based on the candidate's role.
    If source_preference is 'csv_bank' or 'auto' (with matching role in CSV),
    serves targeted questions from interview_questions.csv with expert reference answers!
    """
    skills = candidate_profile.skills if candidate_profile else None

    # Check for matching CSV questions
    csv_candidates = question_manager.get_csv_questions_for_role(
        role=role,
        difficulty=difficulty,
        skills=skills,
    )

    # If the user requested csv_bank, or auto with available questions:
    # 70% chance to pick from the curated 600+ CSV dataset, 30% dynamic AI generation (or 100% CSV if source_preference == 'csv_bank')
    use_csv = (source_preference in ("csv_bank", "csv")) or (source_preference == "auto" and csv_candidates and random.random() < 0.75)

    if use_csv and csv_candidates:
        selected = random.choice(csv_candidates)
        # Ensure role reflects the requested role
        selected.role = role
        return selected

    # Otherwise, generate dynamic question via OmniRoute
    profile_context = ""
    if candidate_profile:
        profile_context = f"""
Candidate Profile:
- Name: {candidate_profile.name}
- Target Role: {candidate_profile.target_role}
- Experience: {candidate_profile.experience_years} years
- Skills: {', '.join(candidate_profile.skills)}
- Areas to improve: {', '.join(candidate_profile.areas_to_improve)}
"""

    # Give the LLM an example from the CSV if available to ground the question
    reference_hint = ""
    if csv_candidates:
        sample_q = random.choice(csv_candidates)
        reference_hint = f"\nFor inspiration, here is a representative technical topic in this domain: '{sample_q.question}'"

    prompt = f"""Generate a high-quality interview question for the following role:
- Target Role: {role}
- Competency Area: {competency or 'Core Technical & Behavioral'}
- Difficulty Level: {difficulty}
{profile_context}{reference_hint}

Respond in JSON format:
{{
    "question": "The interview question text",
    "competency": "Primary competency being assessed",
    "question_type": "technical|behavioral|situational|architecture",
    "expected_competencies": ["list", "of", "competencies"],
    "hints": ["hint for structuring a strong response"],
    "reference_answer": "Key points an expert interviewer looks for in an ideal answer",
    "follow_up_questions": ["probing follow-up question 1", "probing follow-up question 2"]
}}"""

    try:
        response = await llm_client.chat_json(
            messages=[
                {"role": "system", "content": "You are a principal technical interviewer. Generate precise, role-tailored interview questions with reference criteria. Always return valid JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        data = extract_json(response)
        return InterviewQuestion(
            id=str(uuid.uuid4())[:8],
            question=data.get("question", ""),
            role=role,
            competency=data.get("competency", competency or "Core Competency"),
            difficulty=difficulty,
            question_type=data.get("question_type", "technical"),
            expected_competencies=data.get("expected_competencies", []),
            hints=data.get("hints", []),
            reference_answer=data.get("reference_answer", ""),
            follow_up_questions=data.get("follow_up_questions", []),
            source="ai_generated",
        )
    except Exception as e:
        print(f"[QuestionBank] AI generation failed ({e}), falling back to curated bank")
        return get_random_question(role=role, difficulty=difficulty, candidate_profile=candidate_profile)
