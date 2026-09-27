import React, { useState } from 'react'
import ScoreRing from './ScoreRing'

export default function FeedbackPanel({ feedback, mode = 'full', onFollowUp, referenceAnswer }) {
  const [activeTab, setActiveTab] = useState('overview')

  if (!feedback) return null

  const isFull = mode === 'full' && feedback.communication_analysis

  // Fallbacks for scores and text
  const overallScore = feedback.overall_score ?? 0
  const strengths = isFull
    ? (feedback.consolidated_strengths || [])
    : (feedback.strengths || [])
  const improvements = isFull
    ? (feedback.consolidated_improvements || [])
    : (feedback.areas_for_improvement || [])
  const improvedResponse = feedback.improved_response || ''
  const tips = isFull
    ? (feedback.personalized_tips || [])
    : (feedback.coaching_tips || [])
  const followUps = feedback.follow_up_questions || []

  // Full-mode sub-analyses
  const comm = feedback.communication_analysis || {}
  const content = feedback.content_analysis || {}
  const star = feedback.star_analysis || {}

  const getScoreColor = (s) => {
    if (s >= 8) return 'var(--accent-emerald, #10b981)'
    if (s >= 6) return 'var(--accent-blue, #3b82f6)'
    if (s >= 4) return 'var(--accent-amber, #f59e0b)'
    return 'var(--accent-rose, #f43f5e)'
  }

  return (
    <div className="feedback-container">
      {/* Header Banner */}
      <div className="feedback-header">
        <div className="feedback-score-section">
          <ScoreRing score={overallScore} size={130} strokeWidth={9} label="Overall Score" />
        </div>
        <div className="feedback-summary">
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '0.5rem' }}>
            <span className={`badge ${overallScore >= 7 ? 'badge-success' : overallScore >= 5 ? 'badge-warning' : 'badge-danger'}`}>
              {overallScore >= 8 ? 'Excellent Response' : overallScore >= 6 ? 'Solid Answer' : 'Needs Polish'}
            </span>
            <span className="badge badge-primary">
              {isFull ? '🤖 Multi-Agent Orchestration' : '⚡ Quick Evaluation'}
            </span>
          </div>
          <h3>
            {overallScore >= 8
              ? 'Outstanding performance! You effectively addressed the key dimensions.'
              : overallScore >= 6
              ? 'Good structure, with clear opportunities to add impact and precision.'
              : 'Constructive feedback ready to help you elevate your response.'}
          </h3>
          <p className="text-sm text-secondary">
            {isFull
              ? 'Consolidated insights from Communication, Content Depth, STAR Structure, and Interview Coach agents.'
              : 'Rubric-based assessment evaluating relevance, structure, and communication clarity.'}
          </p>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="feedback-tabs">
        <button
          className={`feedback-tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📋 Overview & Strengths
        </button>
        {isFull ? (
          <>
            <button
              className={`feedback-tab ${activeTab === 'comm' ? 'active' : ''}`}
              onClick={() => setActiveTab('comm')}
            >
              💬 Communication ({comm.overall_communication_score ?? '-'})
            </button>
            <button
              className={`feedback-tab ${activeTab === 'content' ? 'active' : ''}`}
              onClick={() => setActiveTab('content')}
            >
              🎯 Content Depth ({content.overall_content_score ?? '-'})
            </button>
            <button
              className={`feedback-tab ${activeTab === 'star' ? 'active' : ''}`}
              onClick={() => setActiveTab('star')}
            >
              ⭐ STAR Structure ({star.star_score ?? '-'})
            </button>
          </>
        ) : (
          <button
            className={`feedback-tab ${activeTab === 'criteria' ? 'active' : ''}`}
            onClick={() => setActiveTab('criteria')}
          >
            📊 Detailed Criteria
          </button>
        )}
        <button
          className={`feedback-tab ${activeTab === 'improved' ? 'active' : ''}`}
          onClick={() => setActiveTab('improved')}
        >
          ✨ Model Answer
        </button>
      </div>

      {/* Tab Content: Overview */}
      {activeTab === 'overview' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1rem' }}>
          <div className="feedback-section">
            <h4>🏆 Key Strengths</h4>
            {strengths.length > 0 ? (
              strengths.map((str, idx) => (
                <div key={idx} className="strength-item">
                  <span className="icon">✓</span>
                  <div>{str}</div>
                </div>
              ))
            ) : (
              <p className="text-sm text-muted">No specific strengths recorded.</p>
            )}
          </div>

          <div className="feedback-section">
            <h4>🎯 Areas for Improvement</h4>
            {improvements.length > 0 ? (
              improvements.map((imp, idx) => (
                <div key={idx} className="improvement-item">
                  <span className="icon">▲</span>
                  <div>{imp}</div>
                </div>
              ))
            ) : (
              <p className="text-sm text-muted">No major improvement areas recorded.</p>
            )}
          </div>

          {tips.length > 0 && (
            <div className="feedback-section" style={{ gridColumn: '1 / -1' }}>
              <h4>💡 Personalized Coaching Tips</h4>
              <ul style={{ paddingLeft: '1.25rem', marginTop: '0.5rem', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {tips.map((tip, idx) => (
                  <li key={idx} className="text-sm" style={{ color: 'var(--text-secondary)' }}>
                    {tip}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Tab Content: Communication (Full Mode) */}
      {activeTab === 'comm' && isFull && (
        <div className="feedback-section">
          <h4>💬 Communication Analysis</h4>
          <p className="text-sm text-secondary" style={{ marginBottom: '1.25rem' }}>
            {comm.feedback || 'Evaluation of delivery clarity, structure, and professional tone.'}
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
            {[
              { label: 'Clarity', val: comm.clarity_score },
              { label: 'Structure', val: comm.structure_score },
              { label: 'Conciseness', val: comm.conciseness_score },
              { label: 'Tone', val: comm.tone_score },
            ].map((item, idx) => (
              <div key={idx} className="card" style={{ padding: '1rem', textAlign: 'center', background: 'var(--bg-glass)' }}>
                <div className="text-sm text-muted">{item.label}</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 800, color: getScoreColor(item.val ?? 0), marginTop: '4px' }}>
                  {item.val ?? '-'} / 10
                </div>
              </div>
            ))}
          </div>

          {comm.suggestions?.length > 0 && (
            <div>
              <h5 style={{ fontSize: '13px', fontWeight: 600, marginBottom: '0.5rem' }}>Actionable Suggestions</h5>
              <ul>
                {comm.suggestions.map((s, i) => (
                  <li key={i} className="text-sm text-secondary" style={{ marginBottom: '4px' }}>• {s}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Tab Content: Content Depth (Full Mode) */}
      {activeTab === 'content' && isFull && (
        <div className="feedback-section">
          <h4>🎯 Content Depth & Accuracy</h4>
          <p className="text-sm text-secondary" style={{ marginBottom: '1.25rem' }}>
            {content.feedback || 'Assessment of technical completeness, relevance, and real-world examples.'}
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
            {[
              { label: 'Relevance', val: content.relevance_score },
              { label: 'Completeness', val: content.completeness_score },
              { label: 'Depth of Knowledge', val: content.knowledge_depth_score },
              { label: 'Evidence & Metrics', val: content.examples_score },
            ].map((item, idx) => (
              <div key={idx} className="card" style={{ padding: '1rem', textAlign: 'center', background: 'var(--bg-glass)' }}>
                <div className="text-sm text-muted">{item.label}</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 800, color: getScoreColor(item.val ?? 0), marginTop: '4px' }}>
                  {item.val ?? '-'} / 10
                </div>
              </div>
            ))}
          </div>

          {content.missing_points?.length > 0 && (
            <div style={{ marginTop: '1rem', padding: '1rem', background: 'rgba(245, 158, 11, 0.08)', borderRadius: 'var(--radius-sm)' }}>
              <h5 style={{ fontSize: '13px', fontWeight: 600, color: 'var(--accent-amber)', marginBottom: '0.5rem' }}>
                Key Missing Points / Topics to Mention
              </h5>
              <ul>
                {content.missing_points.map((pt, i) => (
                  <li key={i} className="text-sm text-secondary" style={{ marginBottom: '4px' }}>• {pt}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Tab Content: STAR Structure (Full Mode) */}
      {activeTab === 'star' && isFull && (
        <div className="feedback-section">
          <h4>⭐ STAR Framework Breakdown</h4>
          <p className="text-sm text-secondary" style={{ marginBottom: '1.25rem' }}>
            {star.structure_feedback || 'Behavioral interview responses thrive when adhering to Situation, Task, Action, and Result.'}
          </p>

          <div className="star-grid" style={{ marginBottom: '1.5rem' }}>
            {[
              { letter: 'S', label: 'Situation', text: star.situation },
              { letter: 'T', label: 'Task', text: star.task },
              { letter: 'A', label: 'Action', text: star.action },
              { letter: 'R', label: 'Result', text: star.result },
            ].map((el, i) => {
              const isPresent = Boolean(el.text && el.text.trim().length > 5)
              return (
                <div key={i} className={`star-item ${isPresent ? 'present' : 'missing'}`}>
                  <div className="star-letter">{el.letter}</div>
                  <div className="star-label">{el.label}</div>
                  <div className="star-status">{isPresent ? '✅' : '❌'}</div>
                  <p className="text-sm text-secondary" style={{ marginTop: '8px', textAlign: 'left', fontSize: '12px' }}>
                    {el.text || 'Not clearly identified in response.'}
                  </p>
                </div>
              )
            })}
          </div>

          {star.restructured_response && (
            <div>
              <h5 style={{ fontSize: '13px', fontWeight: 600, marginBottom: '0.5rem' }}>Restructured into Clean STAR Format</h5>
              <div className="improved-response">
                {star.restructured_response}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Tab Content: Criteria Rubric (Quick Mode) */}
      {activeTab === 'criteria' && !isFull && (
        <div className="feedback-section">
          <h4>📊 Assessment Criteria</h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1rem' }}>
            {(feedback.criteria_scores || []).map((crit, idx) => (
              <div key={idx} className="card" style={{ padding: '1rem', background: 'var(--bg-glass)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                  <span style={{ fontWeight: 600 }}>{crit.criterion}</span>
                  <span style={{ fontWeight: 800, color: getScoreColor(crit.score) }}>{crit.score} / 10</span>
                </div>
                <div className="score-bar" style={{ marginBottom: '8px' }}>
                  <div
                    className="score-bar-fill"
                    style={{
                      width: `${(crit.score / 10) * 100}%`,
                      background: getScoreColor(crit.score),
                    }}
                  />
                </div>
                <p className="text-sm text-secondary">{crit.feedback}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab Content: Improved Model Answer */}
      {activeTab === 'improved' && (
        <div className="feedback-section">
          <h4>✨ High-Scoring Model Answers</h4>
          <p className="text-sm text-secondary" style={{ marginBottom: '1.25rem' }}>
            Compare your response with the official benchmark answer from the curated interview question bank and the AI-elaborated delivery.
          </p>

          {referenceAnswer && (
            <div style={{ marginBottom: '1.5rem', padding: '1.25rem', background: 'rgba(16, 185, 129, 0.06)', border: '1px solid rgba(16, 185, 129, 0.25)', borderRadius: 'var(--radius-sm)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '0.5rem' }}>
                <span style={{ fontSize: '16px' }}>📚</span>
                <span style={{ fontSize: '13px', fontWeight: 700, color: 'var(--accent-emerald)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  Official Benchmark Answer (Interview Question Bank)
                </span>
              </div>
              <p className="text-sm" style={{ color: 'var(--text-primary)', lineHeight: 1.7, whiteSpace: 'pre-wrap' }}>
                {referenceAnswer}
              </p>
            </div>
          )}

          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '0.5rem' }}>
              <span style={{ fontSize: '16px' }}>✨</span>
              <span style={{ fontSize: '13px', fontWeight: 700, color: 'var(--accent-primary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                AI-Coached Elaborated Response
              </span>
            </div>
            <div className="improved-response">
              {improvedResponse || 'An improved response draft will appear here.'}
            </div>
          </div>
        </div>
      )}

      {/* Follow-up Questions Section */}
      {followUps.length > 0 && (
        <div className="feedback-section" style={{ marginTop: '1.5rem' }}>
          <h4>🎯 Recommended Follow-Up Questions</h4>
          <p className="text-sm text-secondary" style={{ marginBottom: '1rem' }}>
            Interviewers frequently ask these probing follow-up questions. Click any question to practice it immediately!
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {followUps.map((q, idx) => (
              <div
                key={idx}
                className="follow-up-item card"
                onClick={() => onFollowUp && onFollowUp(q)}
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '1rem 1.25rem',
                  cursor: 'pointer',
                  background: 'var(--bg-glass)',
                  border: '1px solid var(--border-subtle)',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <span style={{ color: 'var(--accent-primary)', fontWeight: 700 }}>#{idx + 1}</span>
                  <span className="text-sm" style={{ fontWeight: 500 }}>{q}</span>
                </div>
                <span className="arrow btn btn-sm btn-ghost" style={{ padding: '4px 10px' }}>
                  Practice →
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
