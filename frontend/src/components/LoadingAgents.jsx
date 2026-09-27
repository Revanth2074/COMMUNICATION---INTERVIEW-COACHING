import React, { useState, useEffect } from 'react'

export default function LoadingAgents({ mode = 'full' }) {
  const fullAgents = [
    { id: 1, name: 'Communication Analysis Agent', desc: 'Analyzing tone, clarity, and conciseness' },
    { id: 2, name: 'Content Evaluation Agent', desc: 'Evaluating relevance, depth, and domain knowledge' },
    { id: 3, name: 'STAR Structure Agent', desc: 'Validating Situation, Task, Action, Result structure' },
    { id: 4, name: 'Interview Coach Agent', desc: 'Consolidating strengths, improvements & custom plan' },
  ]

  const quickAgents = [
    { id: 1, name: 'Fast Evaluation Agent', desc: 'Scoring against core interview criteria' },
  ]

  const agentList = mode === 'full' ? fullAgents : quickAgents
  const [currentStep, setCurrentStep] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev < agentList.length - 1) return prev + 1
        return prev
      })
    }, 2400)
    return () => clearInterval(interval)
  }, [agentList.length])

  return (
    <div className="card" style={{ marginTop: '2rem', padding: '2rem', textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <div className="loading-spinner" style={{ marginBottom: '1.25rem' }}></div>
      <h3 style={{ fontSize: '1.15rem', fontWeight: 600, marginBottom: '0.5rem' }}>
        {mode === 'full' ? 'Multi-Agent Evaluation in Progress...' : 'Evaluating Response...'}
      </h3>
      <p className="text-sm text-muted" style={{ marginBottom: '1.5rem', maxWidth: '460px' }}>
        {mode === 'full'
          ? 'OmniRoute is orchestrating 4 specialized AI agents simultaneously to deliver comprehensive interview coaching.'
          : 'OmniRoute is rapidly scoring your answer against key interview rubrics.'}
      </p>

      <div className="loading-agents">
        {agentList.map((agent, index) => {
          let statusClass = ''
          let statusText = 'Waiting'
          if (index < currentStep) {
            statusClass = 'done'
            statusText = 'Completed ✓'
          } else if (index === currentStep) {
            statusClass = 'active'
            statusText = 'Analyzing...'
          }

          return (
            <div key={agent.id} className={`agent-status ${statusClass}`}>
              <div className="agent-dot" />
              <div style={{ flex: 1, textAlign: 'left' }}>
                <div style={{ fontWeight: 600, fontSize: '13px' }}>{agent.name}</div>
                <div className="text-muted" style={{ fontSize: '11px' }}>{agent.desc}</div>
              </div>
              <span style={{ fontSize: '11px', fontWeight: 600 }}>{statusText}</span>
            </div>
          )
        })}
      </div>
    </div>
  )
}
