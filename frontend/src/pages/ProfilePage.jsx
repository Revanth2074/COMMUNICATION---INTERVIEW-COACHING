import React, { useState, useEffect } from 'react'

const ROLES = [
  'Software Engineer', 'Java Developer', 'PHP Developer', 'Magento Developer',
  'Backend Developer', 'Full Stack Developer', 'Data Scientist', 'Product Manager',
  'Business Analyst', 'DevOps Engineer', 'Marketing Manager', 'HR Manager',
  'Finance Analyst', 'Consultant', 'UX Designer', 'Project Manager',
]

export default function ProfilePage({ profile, setProfile }) {
  const [formData, setFormData] = useState({
    name: '',
    target_role: 'Software Engineer',
    experience_years: 2,
    skills: ['Python', 'FastAPI', 'React'],
    strengths: ['Problem Solving', 'Team Collaboration'],
    areas_to_improve: ['Conciseness', 'STAR Framework'],
    bio: '',
  })

  const [skillInput, setSkillInput] = useState('')
  const [strengthInput, setStrengthInput] = useState('')
  const [improvementInput, setImprovementInput] = useState('')
  const [savedMessage, setSavedMessage] = useState('')

  useEffect(() => {
    // Load from local storage if available
    const saved = localStorage.getItem('interview_candidate_profile')
    if (saved) {
      try {
        const parsed = JSON.parse(saved)
        setFormData(parsed)
        setProfile(parsed)
      } catch (e) {
        console.error('Error loading saved profile:', e)
      }
    } else if (profile) {
      setFormData(profile)
    }
  }, [])

  const handleAddTag = (field, value, setValue) => {
    if (!value.trim()) return
    if (!formData[field].includes(value.trim())) {
      setFormData({
        ...formData,
        [field]: [...formData[field], value.trim()],
      })
    }
    setValue('')
  }

  const handleRemoveTag = (field, tagToRemove) => {
    setFormData({
      ...formData,
      [field]: formData[field].filter((tag) => tag !== tagToRemove),
    })
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    setProfile(formData)
    localStorage.setItem('interview_candidate_profile', JSON.stringify(formData))
    setSavedMessage('Profile successfully saved! AI agents will tailor questions and coaching to you.')
    setTimeout(() => setSavedMessage(''), 4000)
  }

  return (
    <div className="page">
      <div className="page-header">
        <h1 className="page-title">Candidate Profile</h1>
        <p className="page-subtitle">
          Configure your professional background and development goals so our multi-agent AI can customize coaching to your exact profile.
        </p>
      </div>

      <div className="profile-setup">
        <form onSubmit={handleSubmit} className="card" style={{ padding: '2rem' }}>
          {savedMessage && (
            <div className="badge badge-success mb-4" style={{ display: 'block', padding: '10px 14px', fontSize: '13px' }}>
              ✓ {savedMessage}
            </div>
          )}

          {/* Basic Details */}
          <div className="form-group mb-4">
            <label className="form-label">Full Name</label>
            <input
              type="text"
              className="form-input"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="e.g. Alex Johnson"
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }} className="mb-4">
            <div className="form-group">
              <label className="form-label">Target Role</label>
              <select
                className="form-select"
                value={formData.target_role}
                onChange={(e) => setFormData({ ...formData, target_role: e.target.value })}
              >
                {ROLES.map((r) => (
                  <option key={r} value={r}>
                    {r}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Years of Experience</label>
              <input
                type="number"
                min="0"
                max="40"
                className="form-input"
                value={formData.experience_years}
                onChange={(e) => setFormData({ ...formData, experience_years: parseInt(e.target.value) || 0 })}
              />
            </div>
          </div>

          {/* Technical / Professional Skills */}
          <div className="form-group mb-4">
            <label className="form-label">Skills & Tech Stack</label>
            <div className="skills-input mb-2">
              {formData.skills.map((skill) => (
                <span key={skill} className="skill-tag">
                  {skill}
                  <button type="button" onClick={() => handleRemoveTag('skills', skill)}>
                    ×
                  </button>
                </span>
              ))}
            </div>
            <div style={{ display: 'flex', gap: '8px' }}>
              <input
                type="text"
                className="form-input"
                value={skillInput}
                onChange={(e) => setSkillInput(e.target.value)}
                placeholder="Add a skill (e.g. Distributed Systems, SQL, React)"
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault()
                    handleAddTag('skills', skillInput, setSkillInput)
                  }
                }}
              />
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => handleAddTag('skills', skillInput, setSkillInput)}
              >
                Add
              </button>
            </div>
          </div>

          {/* Known Strengths */}
          <div className="form-group mb-4">
            <label className="form-label">Key Strengths</label>
            <div className="skills-input mb-2">
              {formData.strengths.map((str) => (
                <span key={str} className="skill-tag" style={{ background: 'rgba(16, 185, 129, 0.1)', borderColor: 'rgba(16, 185, 129, 0.3)', color: 'var(--accent-emerald)' }}>
                  {str}
                  <button type="button" onClick={() => handleRemoveTag('strengths', str)}>
                    ×
                  </button>
                </span>
              ))}
            </div>
            <div style={{ display: 'flex', gap: '8px' }}>
              <input
                type="text"
                className="form-input"
                value={strengthInput}
                onChange={(e) => setStrengthInput(e.target.value)}
                placeholder="Add a strength (e.g. System Architecture, Team Mentorship)"
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault()
                    handleAddTag('strengths', strengthInput, setStrengthInput)
                  }
                }}
              />
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => handleAddTag('strengths', strengthInput, setStrengthInput)}
              >
                Add
              </button>
            </div>
          </div>

          {/* Target Areas to Improve */}
          <div className="form-group mb-4">
            <label className="form-label">Areas You Wish to Improve</label>
            <div className="skills-input mb-2">
              {formData.areas_to_improve.map((area) => (
                <span key={area} className="skill-tag" style={{ background: 'rgba(244, 63, 94, 0.1)', borderColor: 'rgba(244, 63, 94, 0.3)', color: 'var(--accent-rose)' }}>
                  {area}
                  <button type="button" onClick={() => handleRemoveTag('areas_to_improve', area)}>
                    ×
                  </button>
                </span>
              ))}
            </div>
            <div style={{ display: 'flex', gap: '8px' }}>
              <input
                type="text"
                className="form-input"
                value={improvementInput}
                onChange={(e) => setImprovementInput(e.target.value)}
                placeholder="Add focus area (e.g. Filler Words, Quantifying Results)"
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault()
                    handleAddTag('areas_to_improve', improvementInput, setImprovementInput)
                  }
                }}
              />
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => handleAddTag('areas_to_improve', improvementInput, setImprovementInput)}
              >
                Add
              </button>
            </div>
          </div>

          {/* Short Bio */}
          <div className="form-group mb-4">
            <label className="form-label">Brief Background / Target Context</label>
            <textarea
              className="form-textarea"
              rows={3}
              value={formData.bio}
              onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
              placeholder="e.g. Preparing for Senior Software Engineer interviews at top tier tech companies. Focus on cloud architecture and cross-team leadership."
            />
          </div>

          <button type="submit" className="btn btn-primary w-full" style={{ padding: '0.85rem' }}>
            💾 Save Profile Settings
          </button>
        </form>
      </div>
    </div>
  )
}
