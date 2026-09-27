import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom'
import { useState, useEffect } from 'react'
import HomePage from './pages/HomePage'
import PracticePage from './pages/PracticePage'
import ProgressPage from './pages/ProgressPage'
import ProfilePage from './pages/ProfilePage'
import './index.css'

function App() {
  const [modelInfo, setModelInfo] = useState({ models: [], default_model: '' })
  const [sessionId, setSessionId] = useState('')
  const [profile, setProfile] = useState(null)

  useEffect(() => {
    // Fetch available models from OmniRoute
    fetch('http://localhost:8000/api/models')
      .then(r => r.json())
      .then(data => setModelInfo(data))
      .catch(err => console.log('Backend not connected yet'))

    // Create a session
    fetch('http://localhost:8000/api/sessions/create', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' })
      .then(r => r.json())
      .then(data => setSessionId(data.session_id))
      .catch(err => console.log('Could not create session'))
  }, [])

  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="navbar-inner">
            <NavLink to="/" className="navbar-brand">
              <div className="navbar-logo">IC</div>
              <div className="navbar-title">
                Interview<span>Coach</span> AI
              </div>
            </NavLink>

            <ul className="navbar-links">
              <li><NavLink to="/" end>Home</NavLink></li>
              <li><NavLink to="/practice">Practice</NavLink></li>
              <li><NavLink to="/progress">Progress</NavLink></li>
              <li><NavLink to="/profile">Profile</NavLink></li>
            </ul>

            <div className="navbar-model">
              <span className="dot"></span>
              <span>{modelInfo.default_model || 'Connecting...'}</span>
            </div>
          </div>
        </nav>

        <div className="app-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/practice" element={<PracticePage sessionId={sessionId} profile={profile} />} />
            <Route path="/progress" element={<ProgressPage sessionId={sessionId} />} />
            <Route path="/profile" element={<ProfilePage profile={profile} setProfile={setProfile} />} />
          </Routes>
        </div>
      </div>
    </Router>
  )
}

export default App
