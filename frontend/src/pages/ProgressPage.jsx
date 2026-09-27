import { useState, useEffect } from 'react'
import ScoreRing from '../components/ScoreRing'

const API_BASE = 'http://localhost:8000/api'

export default function ProgressPage({ sessionId }) {
  const [progress, setProgress] = useState(null)
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (sessionId) {
      loadProgress()
      loadHistory()
    }
  }, [sessionId])

  const loadProgress = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/progress/${sessionId}`)
      if (res.ok) {
        const data = await res.json()
        setProgress(data.progress)
      } else {
        setError('No practice data yet. Start practicing to see your progress!')
      }
    } catch (err) {
      setError('Could not load progress data.')
    }
    setLoading(false)
  }

  const loadHistory = async () => {
    try {
      const res = await fetch(`${API_BASE}/sessions/${sessionId}`)
      if (res.ok) {
        const data = await res.json()
        setHistory(data.history || [])
      }
    } catch (err) {
      console.log('No session history')
    }
  }

  const getScoreColor = (score) => {
    if (score >= 8) return 'var(--accent-emerald)'
    if (score >= 6) return 'var(--accent-blue)'
    if (score >= 4) return 'var(--accent-amber)'
    return 'var(--accent-rose)'
  }

  const getScoreClass = (score) => {
    if (score >= 8) return 'score-excellent'
    if (score >= 6) return 'score-good'
    if (score >= 4) return 'score-average'
    return 'score-poor'
  }

  if (!sessionId) {
    return (
      <div className="page">
        <div className="empty-state">
          <div className="icon">📊</div>
          <h3>No Active Session</h3>
          <p>Start a practice session to begin tracking your progress.</p>
        </div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="page">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <div className="loading-text">Loading your progress...</div>
        </div>
      </div>
    )
  }

  if (error && !progress) {
    return (
      <div className="page">
        <div className="page-header">
          <h1 className="page-title">Progress Tracking</h1>
          <p className="page-subtitle">Track your interview performance over time.</p>
        </div>
        <div className="empty-state">
          <div className="icon">📈</div>
          <h3>No Data Yet</h3>
          <p>{error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">Progress Tracking</h1>
        <p className="page-subtitle">Review your performance trends and improvement areas across practice sessions.</p>
      </div>

      {progress && (
        <>
          {/* Stats Cards */}
          <div className="progress-stats">
            <div className="stat-card">
              <div className="stat-value" style={{ color: 'var(--accent-primary)' }}>
                {progress.total_sessions}
              </div>
              <div className="stat-label">Total Sessions</div>
            </div>
            <div className="stat-card">
              <div className="stat-value" style={{ color: getScoreColor(progress.average_score) }}>
                {progress.average_score.toFixed(1)}
              </div>
              <div className="stat-label">Average Score</div>
            </div>
            <div className="stat-card">
              <div className="stat-value" style={{ color: 'var(--accent-emerald)' }}>
                {progress.top_strengths?.length || 0}
              </div>
              <div className="stat-label">Key Strengths</div>
            </div>
            <div className="stat-card">
              <div className="stat-value" style={{ color: 'var(--accent-amber)' }}>
                {progress.persistent_gaps?.length || 0}
              </div>
              <div className="stat-label">Areas to Improve</div>
            </div>
          </div>

          {/* Score Trend */}
          {progress.score_trend?.length > 0 && (
            <div className="card" style={{ marginBottom: '1.5rem' }}>
              <h3 className="card-title" style={{ marginBottom: '1rem' }}>📈 Score Trend</h3>
              <div style={{ display: 'flex', alignItems: 'flex-end', gap: '8px', height: '160px', padding: '0 1rem' }}>
                {progress.score_trend.map((score, i) => (
                  <div key={i} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '4px' }}>
                    <span className="text-sm font-bold" style={{ color: getScoreColor(score) }}>
                      {score.toFixed(1)}
                    </span>
                    <div
                      style={{
                        width: '100%',
                        maxWidth: '48px',
                        height: `${(score / 10) * 120}px`,
                        borderRadius: '6px 6px 0 0',
                        transition: 'height 600ms cubic-bezier(0.4, 0, 0.2, 1)',
                      }}
                      className={getScoreClass(score)}
                    />
                    <span className="text-sm text-muted">#{i + 1}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="grid-2">
            {/* Strengths */}
            <div className="card">
              <h3 className="card-title" style={{ marginBottom: '1rem' }}>✨ Top Strengths</h3>
              {progress.top_strengths?.length > 0 ? (
                progress.top_strengths.map((s, i) => (
                  <div key={i} className="strength-item">
                    <span className="icon">✅</span>
                    <span>{s}</span>
                  </div>
                ))
              ) : (
                <p className="text-sm text-muted">Complete more sessions to identify strengths.</p>
              )}
            </div>

            {/* Improvement Areas */}
            <div className="card">
              <h3 className="card-title" style={{ marginBottom: '1rem' }}>🎯 Areas to Improve</h3>
              {progress.persistent_gaps?.length > 0 ? (
                progress.persistent_gaps.map((g, i) => (
                  <div key={i} className="improvement-item">
                    <span className="icon">⚠️</span>
                    <span>{g}</span>
                  </div>
                ))
              ) : (
                <p className="text-sm text-muted">Complete more sessions to identify improvement areas.</p>
              )}
            </div>
          </div>

          {/* Recommendations */}
          {progress.recommendations?.length > 0 && (
            <div className="card" style={{ marginTop: '1.5rem' }}>
              <h3 className="card-title" style={{ marginBottom: '1rem' }}>💡 Recommendations</h3>
              {progress.recommendations.map((r, i) => (
                <div key={i} className="strength-item">
                  <span className="icon">💡</span>
                  <span>{r}</span>
                </div>
              ))}
            </div>
          )}
        </>
      )}

      {/* Session History */}
      {history.length > 0 && (
        <div className="card" style={{ marginTop: '1.5rem' }}>
          <h3 className="card-title" style={{ marginBottom: '1rem' }}>📋 Session History</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {history.map((h, i) => (
              <div
                key={i}
                className="glass-panel"
                style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}
              >
                <div
                  style={{
                    width: '40px',
                    height: '40px',
                    borderRadius: 'var(--radius-sm)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontWeight: 800,
                    fontSize: '14px',
                    color: getScoreColor(h.score),
                    background: 'var(--bg-glass)',
                    border: '1px solid var(--border-subtle)',
                  }}
                >
                  {h.score.toFixed(1)}
                </div>
                <div style={{ flex: 1 }}>
                  <p style={{ fontWeight: 600, fontSize: '14px', marginBottom: '2px' }}>
                    {h.question?.substring(0, 80)}{h.question?.length > 80 ? '...' : ''}
                  </p>
                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <span className="badge badge-primary">{h.type === 'full_coaching' ? 'Multi-Agent' : 'Quick'}</span>
                    <span className="text-sm text-muted">
                      {new Date(h.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
