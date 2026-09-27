"""
Multi-Agent Interview Coaching System
Implements specialized agents that communicate through the OmniRoute API:
  1. Interview Question Agent
  2. Communication Analysis Agent
  3. Content Evaluation Agent
  4. STAR/Response Structure Agent
  5. Interview Coach Agent (orchestrator)
"""
import json
from typing import Optional
from models import (
    CandidateProfile, InterviewQuestion, CandidateResponse,
    CommunicationAnalysis, ContentAnalysis, STARAnalysis,
    CoachingFeedback, EvaluationResult, CriterionScore,
)
from llm_client import llm_client, extract_json
from config import settings


# ──────────────────────────────────────────────────────────────
# Agent 1: Interview Question Agent
# ──────────────────────────────────────────────────────────────
class InterviewQuestionAgent:
    """Selects or generates suitable interview questions based on the
    candidate's target role and competency."""

    SYSTEM_PROMPT = """You are an expert Interview Question Specialist. Your role is to:
1. Select or generate highly relevant interview questions
2. Tailor questions to the candidate's target role, experience level, and skills
3. Ensure questions assess the specified competencies
4. Provide hints and expected competencies for each question

Always respond in valid JSON format."""

    async def generate_question(
        self,
        role: str,
        competency: str = "",
        difficulty: str = "intermediate",
        profile: Optional[CandidateProfile] = None,
    ) -> dict:
        profile_info = ""
        if profile:
            profile_info = f"""
Candidate Profile:
- Name: {profile.name}
- Experience: {profile.experience_years} years
- Skills: {', '.join(profile.skills) if profile.skills else 'Not specified'}
- Areas to improve: {', '.join(profile.areas_to_improve) if profile.areas_to_improve else 'Not specified'}
"""

        prompt = f"""Generate an interview question for:
- Target Role: {role}
- Competency: {competency or 'General'}
- Difficulty: {difficulty}
{profile_info}

Respond in JSON:
{{
    "question": "The interview question text",
    "competency": "competency being assessed",
    "question_type": "behavioral|technical|situational|competency|motivational",
    "difficulty": "{difficulty}",
    "expected_competencies": ["list", "of", "expected", "competencies"],
    "hints": ["hint for answering well"],
    "follow_up_questions": ["follow-up question 1", "follow-up question 2"]
}}"""

        response = await llm_client.chat_json(
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
        )
        try:
            return extract_json(response)
        except Exception:
            return {"question": response, "competency": competency, "question_type": "behavioral"}

    async def generate_follow_up(
        self,
        original_question: str,
        candidate_response: str,
        profile: Optional[CandidateProfile] = None,
    ) -> list[str]:
        """Generate personalized follow-up questions based on the candidate's answer."""
        prompt = f"""Based on this interview exchange, generate 3 targeted follow-up questions:

Original Question: {original_question}
Candidate's Response: {candidate_response}

Generate follow-ups that:
1. Probe deeper into areas the candidate mentioned
2. Address any gaps or vague points in their response
3. Test related competencies

Respond in JSON: {{"follow_up_questions": ["q1", "q2", "q3"]}}"""

        response = await llm_client.chat_json(
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        try:
            data = extract_json(response)
            return data.get("follow_up_questions", [])
        except json.JSONDecodeError:
            return []


# ──────────────────────────────────────────────────────────────
# Agent 2: Communication Analysis Agent
# ──────────────────────────────────────────────────────────────
class CommunicationAnalysisAgent:
    """Evaluates clarity, structure, conciseness, and communication quality."""

    SYSTEM_PROMPT = """You are an expert Communication Analyst specializing in interview responses.
Your job is to evaluate the COMMUNICATION QUALITY of a candidate's response, NOT the content accuracy.

Focus on:
- Clarity: Is the message easy to understand?
- Structure: Is the response well-organized with a logical flow?
- Conciseness: Is the response appropriately concise without being too brief?
- Tone: Is the tone professional, confident, and appropriate?

Always respond in valid JSON format with scores from 0-10."""

    async def analyze(self, question: str, response: str) -> CommunicationAnalysis:
        prompt = f"""Analyze the COMMUNICATION QUALITY of this interview response:

Question: {question}
Response: {response}

Evaluate and respond in JSON:
{{
    "clarity_score": 0-10,
    "structure_score": 0-10,
    "conciseness_score": 0-10,
    "tone_score": 0-10,
    "overall_communication_score": 0-10,
    "feedback": "Detailed communication feedback paragraph",
    "suggestions": ["specific suggestion 1", "specific suggestion 2", "specific suggestion 3"]
}}"""

        result = await llm_client.chat_json(
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
        )
        try:
            data = extract_json(result)
            return CommunicationAnalysis(**data)
        except Exception as e:
            print(f"[CommAgent] Parse error: {e}")
            return CommunicationAnalysis(
                clarity_score=5, structure_score=5, conciseness_score=5,
                tone_score=5, overall_communication_score=5,
                feedback="Analysis could not be completed.", suggestions=[]
            )


# ──────────────────────────────────────────────────────────────
# Agent 3: Content Evaluation Agent
# ──────────────────────────────────────────────────────────────
class ContentEvaluationAgent:
    """Evaluates whether the response addresses the question and
    demonstrates relevant knowledge or experience."""

    SYSTEM_PROMPT = """You are an expert Content Evaluator for interview responses.
Your job is to evaluate the CONTENT and SUBSTANCE of a candidate's response.

Focus on:
- Relevance: Does the response directly address the question asked?
- Completeness: Does it cover all important aspects?
- Knowledge Depth: Does it demonstrate genuine expertise or experience?
- Examples: Does it include specific, concrete examples or metrics?

Always respond in valid JSON format with scores from 0-10."""

    async def analyze(
        self,
        question: str,
        response: str,
        expected_competencies: list[str] = None,
        reference_answer: Optional[str] = None,
    ) -> ContentAnalysis:
        competencies_text = ""
        if expected_competencies:
            competencies_text = f"\nExpected competencies to demonstrate: {', '.join(expected_competencies)}"

        reference_text = ""
        if reference_answer:
            reference_text = f"\nIdeal Benchmark Reference Answer (from expert question bank):\n\"{reference_answer}\"\nCompare the candidate's answer with this benchmark answer. Assess accuracy, depth, and identify any missing nuances."

        prompt = f"""Evaluate the CONTENT quality of this interview response:

Question: {question}
Response: {response}
{competencies_text}{reference_text}

Respond in JSON:
{{
    "relevance_score": 0-10,
    "completeness_score": 0-10,
    "knowledge_depth_score": 0-10,
    "examples_score": 0-10,
    "overall_content_score": 0-10,
    "feedback": "Detailed content evaluation paragraph",
    "missing_points": ["point they should have covered 1", "point 2"]
}}"""

        result = await llm_client.chat_json(
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
        )
        try:
            data = extract_json(result)
            return ContentAnalysis(**data)
        except Exception as e:
            print(f"[ContentAgent] Parse error: {e}")
            return ContentAnalysis(
                relevance_score=5, completeness_score=5, knowledge_depth_score=5,
                examples_score=5, overall_content_score=5,
                feedback="Analysis could not be completed.", missing_points=[]
            )


# ──────────────────────────────────────────────────────────────
# Agent 4: STAR/Response Structure Agent
# ──────────────────────────────────────────────────────────────
class STARStructureAgent:
    """Evaluates behavioral responses using the STAR framework
    (Situation, Task, Action, Result)."""

    SYSTEM_PROMPT = """You are an expert in the STAR interview response framework.
Your job is to analyze whether a candidate's response follows the STAR structure:
- Situation: Did they describe the context/background?
- Task: Did they explain their specific responsibility?
- Action: Did they detail the specific actions they took?
- Result: Did they share the outcome/impact with metrics if possible?

Also provide a restructured version of their answer using proper STAR format.
Always respond in valid JSON format."""

    async def analyze(self, question: str, response: str) -> STARAnalysis:
        prompt = f"""Analyze this interview response for STAR structure:

Question: {question}
Response: {response}

Respond in JSON:
{{
    "has_situation": true/false,
    "has_task": true/false,
    "has_action": true/false,
    "has_result": true/false,
    "star_score": 0-10,
    "structure_feedback": "Detailed feedback on response structure",
    "restructured_response": "The response restructured in proper STAR format, maintaining the candidate's content but improving structure"
}}"""

        result = await llm_client.chat_json(
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
        )
        try:
            data = extract_json(result)
            return STARAnalysis(**data)
        except Exception as e:
            print(f"[STARAgent] Parse error: {e}")
            return STARAnalysis(
                star_score=5,
                structure_feedback="Analysis could not be completed.",
                restructured_response=""
            )


# ──────────────────────────────────────────────────────────────
# Agent 5: Interview Coach Agent (Orchestrator)
# ──────────────────────────────────────────────────────────────
class InterviewCoachAgent:
    """Consolidates outputs from all specialist agents and generates
    personalized coaching feedback. Acts as the orchestrator."""

    SYSTEM_PROMPT = """You are a senior Interview Coach who consolidates analysis from multiple
specialist evaluators to provide comprehensive, personalized coaching feedback.

Your role is to:
1. Synthesize communication, content, and structural analysis
2. Identify the candidate's top strengths
3. Prioritize areas for improvement
4. Provide an improved version of their response
5. Create a personalized improvement plan
6. Generate relevant follow-up questions
7. Identify recurring communication or response-quality gaps

Be encouraging but honest. Focus on actionable, specific feedback.
Always respond in valid JSON format."""

    def __init__(self):
        self.question_agent = InterviewQuestionAgent()
        self.communication_agent = CommunicationAnalysisAgent()
        self.content_agent = ContentEvaluationAgent()
        self.star_agent = STARStructureAgent()

    async def evaluate_response(
        self,
        question: str,
        response: str,
        expected_competencies: list[str] = None,
        candidate_profile: Optional[CandidateProfile] = None,
        session_history: list[dict] = None,
        reference_answer: Optional[str] = None,
    ) -> CoachingFeedback:
        """Full multi-agent evaluation pipeline with A2A communication."""

        # Step 1: Run specialist agents in parallel (Agent handoff)
        import asyncio
        comm_task = self.communication_agent.analyze(question, response)
        content_task = self.content_agent.analyze(
            question, response, expected_competencies, reference_answer=reference_answer
        )
        star_task = self.star_agent.analyze(question, response)
        follow_up_task = self.question_agent.generate_follow_up(question, response, candidate_profile)

        comm_analysis, content_analysis, star_analysis, follow_ups = await asyncio.gather(
            comm_task, content_task, star_task, follow_up_task
        )

        # Step 2: Coach consolidation (A2A communication - collecting results)
        history_context = ""
        if session_history:
            scores = [s.get("score", 0) for s in session_history]
            gaps = []
            for s in session_history:
                gaps.extend(s.get("improvements", []))
            if gaps:
                from collections import Counter
                recurring = [g for g, c in Counter(gaps).items() if c >= 2]
                history_context = f"""
Session History:
- Previous scores: {scores}
- Recurring gaps: {recurring}
"""

        profile_context = ""
        if candidate_profile:
            profile_context = f"""
Candidate Profile:
- Name: {candidate_profile.name}
- Target Role: {candidate_profile.target_role}
- Experience: {candidate_profile.experience_years} years
- Skills: {', '.join(candidate_profile.skills) if candidate_profile.skills else 'Not specified'}
"""

        ref_context = ""
        if reference_answer:
            ref_context = f"\nBENCHMARK REFERENCE ANSWER (from expert bank):\n{reference_answer}\n"

        consolidation_prompt = f"""Consolidate the following specialist analyses into comprehensive coaching feedback:

INTERVIEW QUESTION: {question}
CANDIDATE RESPONSE: {response}
{ref_context}

COMMUNICATION ANALYSIS:
- Clarity: {comm_analysis.clarity_score}/10
- Structure: {comm_analysis.structure_score}/10
- Conciseness: {comm_analysis.conciseness_score}/10
- Tone: {comm_analysis.tone_score}/10
- Overall Communication: {comm_analysis.overall_communication_score}/10
- Feedback: {comm_analysis.feedback}
- Suggestions: {comm_analysis.suggestions}

CONTENT ANALYSIS:
- Relevance: {content_analysis.relevance_score}/10
- Completeness: {content_analysis.completeness_score}/10
- Knowledge Depth: {content_analysis.knowledge_depth_score}/10
- Examples: {content_analysis.examples_score}/10
- Overall Content: {content_analysis.overall_content_score}/10
- Feedback: {content_analysis.feedback}
- Missing Points: {content_analysis.missing_points}

STAR STRUCTURE ANALYSIS:
- Situation: {'✓' if star_analysis.has_situation else '✗'}
- Task: {'✓' if star_analysis.has_task else '✗'}
- Action: {'✓' if star_analysis.has_action else '✗'}
- Result: {'✓' if star_analysis.has_result else '✗'}
- STAR Score: {star_analysis.star_score}/10
- Structure Feedback: {star_analysis.structure_feedback}
{profile_context}
{history_context}

Provide consolidated coaching feedback in JSON:
{{
    "overall_score": 0-10 (weighted average considering all analyses),
    "consolidated_strengths": ["strength 1", "strength 2", "strength 3"],
    "consolidated_improvements": ["improvement 1", "improvement 2", "improvement 3"],
    "improved_response": "A complete, improved version of the candidate's response that addresses all identified issues while maintaining their authentic voice",
    "personalized_tips": ["specific actionable tip 1", "tip 2", "tip 3"],
    "improvement_plan": ["Step 1: ...", "Step 2: ...", "Step 3: ..."],
    "recurring_gaps": ["gap that appears across multiple evaluations"]
}}"""

        coaching_result = await llm_client.chat_json(
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": consolidation_prompt},
            ],
            temperature=0.5,
        )

        try:
            data = extract_json(coaching_result)
            return CoachingFeedback(
                overall_score=data.get("overall_score", 5),
                communication_analysis=comm_analysis,
                content_analysis=content_analysis,
                star_analysis=star_analysis,
                consolidated_strengths=data.get("consolidated_strengths", []),
                consolidated_improvements=data.get("consolidated_improvements", []),
                improved_response=data.get("improved_response", ""),
                personalized_tips=data.get("personalized_tips", []),
                follow_up_questions=follow_ups,
                improvement_plan=data.get("improvement_plan", []),
                recurring_gaps=data.get("recurring_gaps", []),
            )
        except (json.JSONDecodeError, Exception) as e:
            print(f"[CoachAgent] Parse error: {e}")
            # Return what we have from specialist agents
            overall = (
                comm_analysis.overall_communication_score * 0.3 +
                content_analysis.overall_content_score * 0.4 +
                star_analysis.star_score * 0.3
            )
            return CoachingFeedback(
                overall_score=round(overall, 1),
                communication_analysis=comm_analysis,
                content_analysis=content_analysis,
                star_analysis=star_analysis,
                consolidated_strengths=["Analysis partially completed"],
                consolidated_improvements=["Please try again for complete feedback"],
                follow_up_questions=follow_ups,
            )

    async def quick_evaluate(
        self,
        question: str,
        response: str,
        reference_answer: Optional[str] = None,
    ) -> EvaluationResult:
        """Simplified single-agent evaluation for quick feedback."""
        ref_text = f"\nBenchmark Reference Answer: {reference_answer}\n" if reference_answer else ""

        prompt = f"""Evaluate this interview response:

Question: {question}
Response: {response}
{ref_text}

Provide evaluation in JSON:
{{
    "overall_score": 0-10,
    "criteria_scores": [
        {{"criterion": "Relevance", "score": 0-10, "weight": 0.20, "feedback": "..."}},
        {{"criterion": "Clarity", "score": 0-10, "weight": 0.15, "feedback": "..."}},
        {{"criterion": "Structure", "score": 0-10, "weight": 0.15, "feedback": "..."}},
        {{"criterion": "Completeness", "score": 0-10, "weight": 0.20, "feedback": "..."}},
        {{"criterion": "Communication Quality", "score": 0-10, "weight": 0.15, "feedback": "..."}},
        {{"criterion": "Examples & Evidence", "score": 0-10, "weight": 0.15, "feedback": "..."}}
    ],
    "strengths": ["strength 1", "strength 2"],
    "areas_for_improvement": ["area 1", "area 2"],
    "improved_response": "An improved version of the response",
    "coaching_tips": ["tip 1", "tip 2"],
    "follow_up_questions": ["follow-up 1", "follow-up 2"]
}}"""

        result = await llm_client.chat_json(
            messages=[
                {"role": "system", "content": "You are an expert interview coach. Evaluate responses and provide structured feedback. Always respond in valid JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
        )

        try:
            data = extract_json(result)
            criteria = [CriterionScore(**c) for c in data.get("criteria_scores", [])]
            return EvaluationResult(
                overall_score=data.get("overall_score", 5),
                criteria_scores=criteria,
                strengths=data.get("strengths", []),
                areas_for_improvement=data.get("areas_for_improvement", []),
                improved_response=data.get("improved_response", ""),
                coaching_tips=data.get("coaching_tips", []),
                follow_up_questions=data.get("follow_up_questions", []),
            )
        except (json.JSONDecodeError, Exception) as e:
            print(f"[QuickEval] Parse error: {e}")
            return EvaluationResult(overall_score=5)


# Global agent instances
question_agent = InterviewQuestionAgent()
coach_agent = InterviewCoachAgent()
