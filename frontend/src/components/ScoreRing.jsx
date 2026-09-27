import React from 'react'

export default function ScoreRing({ score = 0, size = 120, strokeWidth = 8, label = 'Overall' }) {
  const normalizedScore = typeof score === 'number' ? Math.max(0, Math.min(10, score)) : 0
  const percentage = (normalizedScore / 10) * 100
  
  const radius = (size - strokeWidth) / 2
  const circumference = 2 * Math.PI * radius
  const strokeDashoffset = circumference - (percentage / 100) * circumference

  const getColor = (s) => {
    if (s >= 8) return 'var(--accent-emerald, #10b981)'
    if (s >= 6) return 'var(--accent-blue, #3b82f6)'
    if (s >= 4) return 'var(--accent-amber, #f59e0b)'
    return 'var(--accent-rose, #f43f5e)'
  }

  const strokeColor = getColor(normalizedScore)

  return (
    <div className="score-ring" style={{ width: size, height: size }}>
      <svg width={size} height={size}>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="rgba(255, 255, 255, 0.08)"
          strokeWidth={strokeWidth}
          fill="none"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={strokeColor}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          fill="none"
          style={{ transition: 'stroke-dashoffset 1s ease-in-out' }}
        />
      </svg>
      <div style={{ textAlign: 'center', zIndex: 1 }}>
        <div className="score-value" style={{ color: strokeColor }}>
          {normalizedScore.toFixed(1)}
        </div>
        <div className="score-label">{label}</div>
      </div>
    </div>
  )
}
