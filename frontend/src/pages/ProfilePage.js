import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Container, Row, Col, Card, Form, Button, Alert, Badge, ProgressBar } from 'react-bootstrap';
import { 
  FaUser, FaEnvelope, FaBriefcase, FaGraduationCap, FaStar, 
  FaEdit, FaSave, FaEye, FaHistory, FaChartLine
} from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';
import API from '../services/api';
import toast from 'react-hot-toast';

const ProfilePage = () => {
  const { user, setUser } = useAuth();
  const [candidate, setCandidate] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    target_role: '',
    experience_years: 0,
    skills: '',
    competencies: '',
    resume_text: ''
  });
  const [editing, setEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [scores, setScores] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Get candidate profile
        const candidateData = await API.getCurrentCandidate();
        setCandidate(candidateData);
        
        // Set form data
        if (candidateData) {
          setFormData({
            name: candidateData.name || '',
            email: candidateData.email || '',
            target_role: candidateData.target_role || '',
            experience_years: candidateData.experience_years || 0,
            skills: candidateData.skills ? candidateData.skills.join(', ') : '',
            competencies: candidateData.competencies ? candidateData.competencies.join(', ') : '',
            resume_text: candidateData.resume_text || ''
          });
        }
        
        // Get average scores
        if (candidateData) {
          const scoresData = await API.getAverageScores(candidateData.id);
          setScores(scoresData);
        }
        
      } catch (err) {
        setError('Failed to load profile');
        toast.error('Failed to load profile');
      } finally {
        setLoading(false);
      }
    };

    if (user) {
      fetchData();
    }
  }, [user]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSkillsChange = (e) => {
    setFormData(prev => ({
      ...prev,
      skills: e.target.value
    }));
  };

  const handleCompetenciesChange = (e) => {
    setFormData(prev => ({
      ...prev,
      competencies: e.target.value
    }));
  };

  const handleEdit = () => {
    setEditing(true);
  };

  const handleCancel = () => {
    setEditing(false);
    // Reset form data to original values
    if (candidate) {
      setFormData({
        name: candidate.name || '',
        email: candidate.email || '',
        target_role: candidate.target_role || '',
        experience_years: candidate.experience_years || 0,
        skills: candidate.skills ? candidate.skills.join(', ') : '',
        competencies: candidate.competencies ? candidate.competencies.join(', ') : '',
        resume_text: candidate.resume_text || ''
      });
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setError(null);

    try {
      // Prepare candidate data
      const candidateData = {
        name: formData.name,
        email: formData.email,
        target_role: formData.target_role,
        experience_years: parseInt(formData.experience_years) || 0,
        skills: formData.skills 
          .split(',')
          .map(s => s.trim())
          .filter(s => s),
        competencies: formData.competencies
          .split(',')
          .map(c => c.trim())
          .filter(c => c),
        resume_text: formData.resume_text
      };

      // Update candidate
      const response = await API.updateCandidate(candidate.id, candidateData);
      
      if (response.success) {
        // Update local candidate data
        setCandidate(response.data);
        setEditing(false);
        toast.success('Profile updated successfully!');
      } else {
        setError(response.message || 'Failed to update profile');
      }
      
    } catch (err) {
      setError('Failed to update profile');
      toast.error('Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'success';
    if (score >= 60) return 'warning';
    return 'danger';
  };

  if (loading) {
    return (
      <Container fluid className="spinner-container py-5">
        <div className="loading-spinner"></div>
        <p className="mt-3">Loading your profile...</p>
      </Container>
    );
  }

  if (error) {
    return (
      <Container fluid className="py-5">
        <Alert variant="danger">{error}</Alert>
      </Container>
    );
  }

  return (
    <div className="fade-in">
      {/* Header */}
      <section className="page-header">
        <h1>
          <FaUser className="me-3" />
          Your Profile
        </h1>
        <p>Manage your candidate information and preferences</p>
      </section>

      <Row className="g-4">
        {/* Profile Card */}
        <Col lg={8}>
          <Card>
            <Card.Header className="d-flex justify-content-between align-items-center">
              <span>
                <FaUser className="me-2" />
                Candidate Information
              </span>
              {!editing ? (
                <Button variant="outline-primary" size="sm" onClick={handleEdit}>
                  <FaEdit className="me-2" />
                  Edit Profile
                </Button>
              ) : (
                <div>
                  <Button 
                    variant="success" 
                    size="sm" 
                    onClick={handleSave}
                    disabled={saving}
                    className="me-2"
                  >
                    {saving ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                        Saving...
                      </>
                    ) : (
                      <>
                        <FaSave className="me-2" />
                        Save Changes
                      </>
                    )}
                  </Button>
                  <Button 
                    variant="outline-secondary" 
                    size="sm" 
                    onClick={handleCancel}
                  >
                    Cancel
                  </Button>
                </div>
              )}
            </Card.Header>
            
            <Card.Body>
              {error && (
                <Alert variant="danger" className="mb-4">
                  {error}
                </Alert>
              )}

              <Form>
                <Row className="g-3">
                  <Col md={6}>
                    <Form.Group>
                      <Form.Label>
                        <FaUser className="me-2" />
                        Full Name
                      </Form.Label>
                      <Form.Control
                        type="text"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        placeholder="Enter your full name"
                        disabled={!editing}
                      />
                    </Form.Group>
                  </Col>
                  
                  <Col md={6}>
                    <Form.Group>
                      <Form.Label>
                        <FaEnvelope className="me-2" />
                        Email
                      </Form.Label>
                      <Form.Control
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        placeholder="Enter your email"
                        disabled={!editing}
                      />
                    </Form.Group>
                  </Col>
                  
                  <Col md={6}>
                    <Form.Group>
                      <Form.Label>
                        <FaBriefcase className="me-2" />
                        Target Role
                      </Form.Label>
                      <Form.Control
                        type="text"
                        name="target_role"
                        value={formData.target_role}
                        onChange={handleChange}
                        placeholder="e.g., Software Engineer, Product Manager"
                        disabled={!editing}
                      />
                    </Form.Group>
                  </Col>
                  
                  <Col md={6}>
                    <Form.Group>
                      <Form.Label>
                        <FaGraduationCap className="me-2" />
                        Years of Experience
                      </Form.Label>
                      <Form.Control
                        type="number"
                        name="experience_years"
                        value={formData.experience_years}
                        onChange={handleChange}
                        min="0"
                        max="50"
                        disabled={!editing}
                      />
                    </Form.Group>
                  </Col>
                  
                  <Col md={12}>
                    <Form.Group>
                      <Form.Label>
                        <FaStar className="me-2" />
                        Skills (comma separated)
                      </Form.Label>
                      <Form.Control
                        type="text"
                        name="skills"
                        value={formData.skills}
                        onChange={handleSkillsChange}
                        placeholder="e.g., Python, JavaScript, Project Management"
                        disabled={!editing}
                      />
                      <Form.Text className="text-muted">
                        Separate multiple skills with commas
                      </Form.Text>
                    </Form.Group>
                  </Col>
                  
                  <Col md={12}>
                    <Form.Group>
                      <Form.Label>
                        Competencies (comma separated)
                      </Form.Label>
                      <Form.Control
                        type="text"
                        name="competencies"
                        value={formData.competencies}
                        onChange={handleCompetenciesChange}
                        placeholder="e.g., Communication, Problem Solving, Leadership"
                        disabled={!editing}
                      />
                      <Form.Text className="text-muted">
                        Separate multiple competencies with commas
                      </Form.Text>
                    </Form.Group>
                  </Col>
                  
                  <Col md={12}>
                    <Form.Group>
                      <Form.Label>Resume / Bio</Form.Label>
                      <Form.Control
                        as="textarea"
                        rows={4}
                        name="resume_text"
                        value={formData.resume_text}
                        onChange={handleChange}
                        placeholder="Brief description of your experience, education, and skills..."
                        disabled={!editing}
                      />
                    </Form.Group>
                  </Col>
                </Row>
              </Form>
            </Card.Body>
          </Card>

          {/* Performance Summary */}
          {scores && (
            <Card className="mt-4">
              <Card.Header>
                <FaChartLine className="me-2" />
                Your Performance Summary
              </Card.Header>
              <Card.Body>
                <Row className="g-3">
                  <Col md={3}>
                    <div className="text-center">
                      <h4 className="text-primary">{Math.round(scores.overall || 0)}</h4>
                      <p className="mb-0">Overall Score</p>
                      <ProgressBar 
                        now={scores.overall || 0} 
                        max={100}
                        variant={getScoreColor(scores.overall || 0)}
                        className="mt-2"
                      />
                    </div>
                  </Col>
                  <Col md={3}>
                    <div className="text-center">
                      <h4 className="text-success">{Math.round(scores.relevance || 0)}</h4>
                      <p className="mb-0">Relevance</p>
                      <ProgressBar 
                        now={scores.relevance || 0} 
                        max={100}
                        variant={getScoreColor(scores.relevance || 0)}
                        className="mt-2"
                      />
                    </div>
                  </Col>
                  <Col md={3}>
                    <div className="text-center">
                      <h4 className="text-info">{Math.round(scores.clarity || 0)}</h4>
                      <p className="mb-0">Clarity</p>
                      <ProgressBar 
                        now={scores.clarity || 0} 
                        max={100}
                        variant={getScoreColor(scores.clarity || 0)}
                        className="mt-2"
                      />
                    </div>
                  </Col>
                  <Col md={3}>
                    <div className="text-center">
                      <h4 className="text-warning">{Math.round(scores.structure || 0)}</h4>
                      <p className="mb-0">Structure</p>
                      <ProgressBar 
                        now={scores.structure || 0} 
                        max={100}
                        variant={getScoreColor(scores.structure || 0)}
                        className="mt-2"
                      />
                    </div>
                  </Col>
                </Row>
                
                <div className="text-center mt-4">
                  <Link to="/progress">
                    <Button variant="outline-primary">
                      <FaChartLine className="me-2" />
                      View Detailed Progress
                    </Button>
                  </Link>
                </div>
              </Card.Body>
            </Card>
          )}
        </Col>

        {/* Quick Actions */}
        <Col lg={4}>
          <Card className="mb-4">
            <Card.Header>
              <FaStar className="me-2" />
              Quick Actions
            </Card.Header>
            <Card.Body>
              <div className="d-grid gap-2">
                <Link to="/practice">
                  <Button variant="primary" className="w-100 py-2">
                    <FaEdit className="me-2" />
                    Start Practicing
                  </Button>
                </Link>
                
                <Link to="/history">
                  <Button variant="outline-primary" className="w-100 py-2">
                    <FaHistory className="me-2" />
                    View History
                  </Button>
                </Link>
                
                <Link to="/progress">
                  <Button variant="outline-primary" className="w-100 py-2">
                    <FaChartLine className="me-2" />
                    Track Progress
                  </Button>
                </Link>
                
                <Link to="/dashboard">
                  <Button variant="outline-primary" className="w-100 py-2">
                    <FaEye className="me-2" />
                    Go to Dashboard
                  </Button>
                </Link>
              </div>
            </Card.Body>
          </Card>

          {/* User Account Info */}
          <Card>
            <Card.Header>
              <FaUser className="me-2" />
              Account Information
            </Card.Header>
            <Card.Body>
              <dl className="row">
                <dt className="col-sm-4">Username:</dt>
                <dd className="col-sm-8">{user?.username || 'N/A'}</dd>
                
                <dt className="col-sm-4">Email:</dt>
                <dd className="col-sm-8">{user?.email || 'N/A'}</dd>
                
                <dt className="col-sm-4">Full Name:</dt>
                <dd className="col-sm-8">{user?.full_name || 'Not provided'}</dd>
                
                <dt className="col-sm-4">Account Type:</dt>
                <dd className="col-sm-8">
                  <Badge bg={user?.is_admin ? 'warning' : 'primary' }>
                    {user?.is_admin ? 'Administrator' : 'Standard User'}
                  </Badge>
                </dd>
                
                <dt className="col-sm-4">Member Since:</dt>
                <dd className="col-sm-8">
                  {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                </dd>
              </dl>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default ProfilePage;
