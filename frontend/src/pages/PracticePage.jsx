import { useState, useEffect, useRef } from 'react'
import ScoreRing from '../components/ScoreRing'
import FeedbackPanel from '../components/FeedbackPanel'
import LoadingAgents from '../components/LoadingAgents'

const API_BASE = 'http://localhost:8000/api'

const ROLES = [
  'Software Engineer', 'Java Developer', 'PHP Developer', 'Magento Developer',
  'Backend Developer', 'Full Stack Developer', 'Data Scientist', 'Product Manager',
  'Business Analyst', 'DevOps Engineer', 'Marketing Manager', 'HR Manager',
  'Finance Analyst', 'Consultant', 'UX Designer', 'Project Manager',
]

const DIFFICULTIES = ['entry', 'intermediate', 'advanced', 'expert']
const QUESTION_TYPES = ['behavioral', 'technical', 'situational', 'competency', 'motivational']
const QUESTION_SOURCES = [
  { value: 'auto', label: '🎯 Smart Auto' },
  { value: 'csv_bank', label: '📚 Question Bank (CSV)' },
  { value: 'ai_generated', label: '🤖 AI Generated' },
]

export default function PracticePage({ sessionId, profile }) {
  const [role, setRole] = useState('Java Developer')
  const [difficulty, setDifficulty] = useState('intermediate')
  const [questionType, setQuestionType] = useState('')
  const [sourcePreference, setSourcePreference] = useState('auto')
  const [question, setQuestion] = useState(null)
  const [response, setResponse] = useState('')
  const [loading, setLoading] = useState(false)
  const [evaluating, setEvaluating] = useState(false)
  const [feedback, setFeedback] = useState(null)
  const [evaluationMode, setEvaluationMode] = useState('full') // 'quick' or 'full'
  const [isRecording, setIsRecording] = useState(false)
  const [showHints, setShowHints] = useState(false)
  const textareaRef = useRef(null)

  const fetchQuestion = async () => {
    setLoading(true)
    setFeedback(null)
    setResponse('')
    try {
      const res = await fetch(`${API_BASE}/questions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          role,
          difficulty,
          question_type: questionType || undefined,
          candidate_profile: profile || undefined,
          source_preference: sourcePreference,
        }),
      })
      const data = await res.json()
      setQuestion(data.question)
    } catch (err) {
      console.error('Error fetching question:', err)
      // Fallback question
      setQuestion({
        question: 'Tell me about yourself and your experience.',
        role: role,
        competency: 'Communication',
        difficulty,
        question_type: 'behavioral',
        expected_competencies: ['communication', 'self-awareness'],
        hints: ['Keep it concise (1-2 minutes)', 'Focus on relevant experience'],
        follow_up_questions: [],
      })
    }
    setLoading(false)
  }

  const submitResponse = async () => {
    if (!response.trim() || !question) return
    setEvaluating(true)
    setFeedback(null)

    const endpoint = evaluationMode === 'full' ? '/coach' : '/evaluate'
    try {
      const res = await fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: question.question,
          response: response,
          question_id: question.id || '',
          expected_competencies: question.expected_competencies || [],
          candidate_profile: profile || undefined,
          session_id: sessionId || '',
          reference_answer: question.reference_answer || '',
        }),
      })
      const data = await res.json()
      setFeedback(evaluationMode === 'full' ? data.coaching : data.evaluation)
    } catch (err) {
      console.error('Evaluation error:', err)
    }
    setEvaluating(false)
  }

  const handleFollowUp = (followUpQuestion) => {
    setQuestion({
      ...question,
      question: followUpQuestion,
      hints: [],
      follow_up_questions: [],
    })
    setResponse('')
    setFeedback(null)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const handleVoiceInput = () => {
    if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
      alert('Speech recognition not supported in this browser. Please use Chrome.')
      return
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    const recognition = new SpeechRecognition()
    recognition.continuous = true
    recognition.interimResults = true
    recognition.lang = 'en-US'

    if (isRecording) {
      recognition.stop()
      setIsRecording(false)
      return
    }

    setIsRecording(true)
    recognition.start()

    recognition.onresult = (event) => {
      let transcript = ''
      for (let i = 0; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript
      }
      setResponse(transcript)
    }

    recognition.onerror = () => {
      setIsRecording(false)
    }

    recognition.onend = () => {
      setIsRecording(false)
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">Interview Practice</h1>
        <p className="page-subtitle">
          Select your target role and difficulty, then practice with AI-generated questions and receive multi-agent feedback.
        </p>
      </div>

      {/* Configuration Bar */}
      <div className="card mb-4" style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '1rem', alignItems: 'flex-end' }}>
          <div className="form-group" style={{ flex: '1 1 180px', marginBottom: 0 }}>
            <label className="form-label">Target Role</label>
            <select className="form-select" value={role} onChange={e => setRole(e.target.value)}>
              {ROLES.map(r => <option key={r} value={r}>{r}</option>)}
            </select>
          </div>
          <div className="form-group" style={{ flex: '1 1 130px', marginBottom: 0 }}>
            <label className="form-label">Difficulty</label>
            <select className="form-select" value={difficulty} onChange={e => setDifficulty(e.target.value)}>
              {DIFFICULTIES.map(d => <option key={d} value={d}>{d.charAt(0).toUpperCase() + d.slice(1)}</option>)}
            </select>
          </div>
          <div className="form-group" style={{ flex: '1 1 160px', marginBottom: 0 }}>
            <label className="form-label">Question Source</label>
            <select className="form-select" value={sourcePreference} onChange={e => setSourcePreference(e.target.value)}>
              {QUESTION_SOURCES.map(s => <option key={s.value} value={s.value}>{s.label}</option>)}
            </select>
          </div>
          <div className="form-group" style={{ flex: '1 1 130px', marginBottom: 0 }}>
            <label className="form-label">Question Type</label>
            <select className="form-select" value={questionType} onChange={e => setQuestionType(e.target.value)}>
              <option value="">Any Type</option>
              {QUESTION_TYPES.map(t => <option key={t} value={t}>{t.charAt(0).toUpperCase() + t.slice(1)}</option>)}
            </select>
          </div>
          <div className="form-group" style={{ flex: '0 0 auto', marginBottom: 0 }}>
            <label className="form-label">Evaluation</label>
            <div style={{ display: 'flex', gap: '4px', background: 'var(--bg-glass)', border: '1px solid var(--border-subtle)', borderRadius: 'var(--radius-sm)', padding: '3px' }}>
              <button
                className={`btn btn-sm ${evaluationMode === 'full' ? 'btn-primary' : 'btn-ghost'}`}
                onClick={() => setEvaluationMode('full')}
                style={{ padding: '6px 12px' }}
              >
                🤖 Multi-Agent
              </button>
              <button
                className={`btn btn-sm ${evaluationMode === 'quick' ? 'btn-primary' : 'btn-ghost'}`}
                onClick={() => setEvaluationMode('quick')}
                style={{ padding: '6px 12px' }}
              >
                ⚡ Quick
              </button>
            </div>
          </div>
          <button
            className="btn btn-primary"
            onClick={fetchQuestion}
            disabled={loading}
          >
            {loading ? '⏳ Loading...' : '🎯 Get Question'}
          </button>
        </div>
      </div>

      {/* Main Practice Area */}
      {question && (
        <div className="practice-layout">
          {/* Question Card */}
          <div className="question-card">
            <div className="question-meta">
              <span className="badge badge-primary">{question.role || role}</span>
              {question.source === 'interview_questions.csv' ? (
                <span className="badge badge-success">📚 CSV Bank ({question.language || 'Verified'})</span>
              ) : (
                <span className="badge badge-info">✨ AI Generated</span>
              )}
              <span className="badge badge-warning">{question.difficulty}</span>
              {question.competency && (
                <span className="badge badge-secondary">{question.competency}</span>
              )}
            </div>
            <p className="question-text">{question.question}</p>

            {question.expected_competencies?.length > 0 && (
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.375rem', marginBottom: '0.75rem' }}>
                <span className="text-sm text-muted" style={{ marginRight: '4px' }}>Expected:</span>
                {question.expected_competencies.map((c, i) => (
                  <span key={i} className="tag">{c}</span>
                ))}
              </div>
            )}

            {question.hints?.length > 0 && (
              <>
                <button
                  className="btn btn-ghost btn-sm"
                  onClick={() => setShowHints(!showHints)}
                  style={{ marginTop: '0.5rem' }}
                >
                  💡 {showHints ? 'Hide Hints' : 'Show Hints'}
                </button>
                {showHints && (
                  <div className="question-hints">
                    <h4>💡 Hints</h4>
                    <ul>
                      {question.hints.map((h, i) => <li key={i}>{h}</li>)}
                    </ul>
                  </div>
                )}
              </>
            )}
          </div>

          {/* Response Area */}
          <div className="response-card">
            <div className="form-group" style={{ marginBottom: '0.75rem' }}>
              <label className="form-label">Your Response</label>
              <textarea
                ref={textareaRef}
                className="form-textarea"
                value={response}
                onChange={e => setResponse(e.target.value)}
                placeholder="Type your interview response here... Be detailed and specific. Use the STAR method for behavioral questions."
                style={{ minHeight: '220px' }}
              />
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span className="text-sm text-muted">
                {response.split(/\s+/).filter(Boolean).length} words
              </span>
              <div className="response-actions">
                <button
                  className={`btn btn-secondary voice-btn ${isRecording ? 'recording' : ''}`}
                  onClick={handleVoiceInput}
                  title={isRecording ? 'Stop recording' : 'Start voice input'}
                >
                  {isRecording ? '⏹️ Stop' : '🎤 Voice'}
                </button>
                <button
                  className="btn btn-primary"
                  onClick={submitResponse}
                  disabled={!response.trim() || evaluating}
                >
                  {evaluating ? '⏳ Analyzing...' : evaluationMode === 'full' ? '🧠 Get Full Coaching' : '⚡ Quick Evaluate'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* No Question State */}
      {!question && !loading && (
        <div className="empty-state">
          <div className="icon">🎯</div>
          <h3>Ready to Practice?</h3>
          <p>Select your target role and click "Get Question" to start your interview practice session.</p>
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <div className="loading-text">Generating a tailored question for you...</div>
        </div>
      )}

      {/* Evaluating State with Agent Status */}
      {evaluating && <LoadingAgents mode={evaluationMode} />}

      {/* Feedback Results */}
      {feedback && !evaluating && (
        <FeedbackPanel
          feedback={feedback}
          mode={evaluationMode}
          onFollowUp={handleFollowUp}
          referenceAnswer={question?.reference_answer}
        />
      )}
    </div>
  )
}
