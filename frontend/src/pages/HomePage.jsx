import { useNavigate } from 'react-router-dom'

const features = [
  {
    icon: '🎯',
    iconClass: 'purple',
    title: 'Smart Question Selection',
    description: 'AI-powered questions tailored to your target role, experience level, and competency areas.',
  },
  {
    icon: '🧠',
    iconClass: 'emerald',
    title: 'Multi-Agent Analysis',
    description: 'Five specialized AI agents analyze your response from communication, content, and structural perspectives.',
  },
  {
    icon: '📊',
    iconClass: 'cyan',
    title: 'STAR Framework Analysis',
    description: 'Automatic evaluation of your behavioral responses using the Situation-Task-Action-Result method.',
  },
  {
    icon: '💬',
    iconClass: 'amber',
    title: 'Communication Coaching',
    description: 'Detailed feedback on clarity, tone, conciseness, and overall communication quality.',
  },
  {
    icon: '📈',
    iconClass: 'rose',
    title: 'Progress Tracking',
    description: 'Track your improvement across sessions with score trends and personalized improvement plans.',
  },
  {
    icon: '🎤',
    iconClass: 'blue',
    title: 'Voice & Text Input',
    description: 'Practice with text responses or record your voice for a more realistic interview simulation.',
  },
]

export default function HomePage() {
  const navigate = useNavigate()

  return (
    <div>
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-badge">
          ✨ Powered by Multi-Agent AI through OmniRoute
        </div>
        <h1 className="hero-title">
          Master Your Interviews with{' '}
          <span className="gradient-text">AI-Powered Coaching</span>
        </h1>
        <p className="hero-subtitle">
          Practice interview questions, receive real-time structured feedback from
          5 specialized AI agents, and track your improvement over time.
        </p>
        <div className="hero-actions">
          <button className="btn btn-primary btn-lg" onClick={() => navigate('/practice')}>
            🚀 Start Practicing
          </button>
          <button className="btn btn-secondary btn-lg" onClick={() => navigate('/profile')}>
            👤 Set Up Profile
          </button>
        </div>
        <div className="hero-stats">
          <div className="hero-stat">
            <div className="hero-stat-value">25+</div>
            <div className="hero-stat-label">Curated Questions</div>
          </div>
          <div className="hero-stat">
            <div className="hero-stat-value">5</div>
            <div className="hero-stat-label">AI Agents</div>
          </div>
          <div className="hero-stat">
            <div className="hero-stat-value">12</div>
            <div className="hero-stat-label">Role Categories</div>
          </div>
          <div className="hero-stat">
            <div className="hero-stat-value">6</div>
            <div className="hero-stat-label">Evaluation Criteria</div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="features-section">
        <div className="grid-3">
          {features.map((f, i) => (
            <div
              key={i}
              className="feature-card"
              onClick={() => navigate('/practice')}
            >
              <div className={`feature-icon ${f.iconClass}`}>{f.icon}</div>
              <h3 className="feature-title">{f.title}</h3>
              <p className="feature-description">{f.description}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
