import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Container, Row, Col, Card, Button, Badge, ProgressBar, ListGroup } from 'react-bootstrap';
import { 
  FaChartLine, FaPlayCircle, FaHistory, FaUser, FaBrain, 
  FaComments, FaStar, FaArrowRight, FaTrophy, FaFire, FaClock
} from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';
import API from '../services/api';
import toast from 'react-hot-toast';

const DashboardPage = () => {
  const { user } = useAuth();
  const [candidate, setCandidate] = useState(null);
  const [feedback, setFeedback] = useState([]);
  const [scores, setScores] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch candidate profile
        const candidateData = await API.getCurrentCandidate();
        setCandidate(candidateData);

        // Fetch recent feedback
        if (candidateData) {
          const feedbackData = await API.getFeedbackByCandidate(candidateData.id, { page_size: 5 });
          setFeedback(feedbackData.data || []);

          // Fetch average scores
          const scoresData = await API.getAverageScores(candidateData.id);
          setScores(scoresData);
        }
      } catch (err) {
        setError('Failed to load dashboard data');
        toast.error('Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    if (user) {
      fetchData();
    }
  }, [user]);

  const quickActions = [
    {
      title: 'Start Practice',
      description: 'Answer interview questions and get feedback',
      icon: <FaPlayCircle />,
      color: '#667eea',
      link: '/practice'
    },
    {
      title: 'View History',
      description: 'Review your past practice sessions',
      icon: <FaHistory />,
      color: '#f093fb',
      link: '/history'
    },
    {
      title: 'Track Progress',
      description: 'Monitor your improvement over time',
      icon: <FaChartLine />,
      color: '#43e97b',
      link: '/progress'
    },
    {
      title: 'Edit Profile',
      description: 'Update your candidate information',
      icon: <FaUser />,
      color: '#fa709a',
      link: '/profile'
    }
  ];

  const agentStats = [
    {
      name: 'Communication',
      icon: <FaComments />,
      color: '#667eea',
      score: scores?.clarity || 0
    },
    {
      name: 'Content',
      icon: <FaBrain />,
      color: '#f093fb',
      score: scores?.relevance || 0
    },
    {
      name: 'Structure',
      icon: <FaStar />,
      color: '#43e97b',
      score: scores?.structure || 0
    },
    {
      name: 'Overall',
      icon: <FaTrophy />,
      color: '#fa709a',
      score: scores?.overall || 0
    }
  ];

  const getPerformanceLevel = (score) => {
    if (score >= 90) return { level: 'Excellent', color: 'success' };
    if (score >= 80) return { level: 'Good', color: 'primary' };
    if (score >= 70) return { level: 'Satisfactory', color: 'warning' };
    if (score >= 60) return { level: 'Developing', color: 'danger' };
    return { level: 'Needs Improvement', color: 'danger' };
  };

  if (loading) {
    return (
      <Container fluid className="spinner-container py-5">
        <div className="loading-spinner"></div>
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
      {/* Welcome Section */}
      <section className="page-header">
        <h1>Welcome back, {user?.username || 'User'}!</h1>
        <p>
          {candidate ? (
            <>
              You're practicing for <strong>{candidate.target_role}</strong> role
              {candidate.experience_years > 0 && (
                <>, with {candidate.experience_years} years of experience</>
              )}
            </>
          ) : (
            'Complete your profile to get personalized recommendations'
          )}
        </p>
      </section>

      {/* Quick Actions */}
      <section className="mb-5">
        <h2 className="section-title">Quick Actions</h2>
        <Row className="g-4">
          {quickActions.map((action, index) => (
            <Col md={3} key={index}>
              <Card className="h-100 action-card">
                <Card.Body className="text-center">
                  <div 
                    className="agent-icon mx-auto mb-3"
                    style={{ background: `linear-gradient(135deg, ${action.color} 0%, ${action.color}dd 100%)` }}
                  >
                    <span style={{ color: 'white' }}>
                      {action.icon}
                    </span>
                  </div>
                  <Card.Title as="h5" className="mb-2">{action.title}</Card.Title>
                  <Card.Text className="text-muted small mb-3">
                    {action.description}
                  </Card.Text>
                  <Link to={action.link}>
                    <Button variant="outline-primary" size="sm">
                      Go to {action.title.split(' ')[0]}
                      <FaArrowRight className="ms-2" />
                    </Button>
                  </Link>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      </section>

      {/* Performance Overview */}
      {scores && (
        <section className="mb-5">
          <h2 className="section-title">Performance Overview</h2>
          <Row className="g-4">
            {agentStats.map((stat, index) => (
              <Col md={3} key={index}>
                <Card className="h-100">
                  <Card.Body>
                    <div className="d-flex align-items-center mb-3">
                      <span 
                        className="me-3" 
                        style={{ color: stat.color, fontSize: '1.5rem' }}
                      >
                        {stat.icon}
                      </span>
                      <div>
                        <Card.Title as="h6" className="mb-0">{stat.name}</Card.Title>
                        <div className="d-flex align-items-center">
                          <span className="score-badge me-2">{Math.round(stat.score)}</span>
                          <Badge bg={getPerformanceLevel(stat.score).color}>
                            {getPerformanceLevel(stat.score).level}
                          </Badge>
                        </div>
                      </div>
                    </div>
                    <ProgressBar 
                      now={stat.score} 
                      max={100}
                      variant={getPerformanceLevel(stat.score).color}
                      className="mb-2"
                    />
                    <small className="text-muted">{Math.round(stat.score)}/100</small>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        </section>
      )}

      {/* Recent Activity */}
      {feedback.length > 0 && (
        <section className="mb-5">
          <h2 className="section-title">Recent Activity</h2>
          <Row>
            <Col>
              <ListGroup variant="flush">
                {feedback.slice(0, 5).map((item, index) => (
                  <ListGroup.Item key={index} className="d-flex align-items-center">
                    <div className="flex-grow-1">
                      <div className="d-flex justify-content-between align-items-center">
                        <strong>Session #{item.session_id || index + 1}</strong>
                        <Badge bg="primary">
                          {Math.round(item.overall_score || 0)}%
                        </Badge>
                      </div>
                      <small className="text-muted">
                        {new Date(item.created_at).toLocaleDateString()}
                      </small>
                    </div>
                  </ListGroup.Item>
                ))}
              </ListGroup>
              <div className="text-center mt-3">
                <Link to="/history">
                  <Button variant="outline-primary">
                    View All Sessions
                  </Button>
                </Link>
              </div>
            </Col>
          </Row>
        </section>
      )}

      {/* Tips Section */}
      <section className="mb-5">
        <h2 className="section-title">Quick Tips</h2>
        <Row className="g-4">
          <Col md={4}>
            <Card className="h-100 border-primary">
              <Card.Body>
                <div className="d-flex align-items-center mb-3">
                  <FaBrain className="me-3" style={{ color: '#667eea', fontSize: '1.5rem' }} />
                  <Card.Title as="h6" className="mb-0">Use the STAR Method</Card.Title>
                </div>
                <Card.Text>
                  Structure your answers using Situation, Task, Action, Result for behavioral questions.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
          
          <Col md={4}>
            <Card className="h-100 border-success">
              <Card.Body>
                <div className="d-flex align-items-center mb-3">
                  <FaComments className="me-3" style={{ color: '#43e97b', fontSize: '1.5rem' }} />
                  <Card.Title as="h6" className="mb-0">Be Clear and Concise</Card.Title>
                </div>
                <Card.Text>
                  Focus on delivering clear, structured responses that directly address the question.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
          
          <Col md={4}>
            <Card className="h-100 border-warning">
              <Card.Body>
                <div className="d-flex align-items-center mb-3">
                  <FaClock className="me-3" style={{ color: '#fa709a', fontSize: '1.5rem' }} />
                  <Card.Title as="h6" className="mb-0">Practice Regularly</Card.Title>
                </div>
                <Card.Text>
                  Consistent practice is key to improving your interview skills and confidence.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </section>
    </div>
  );
};

export default DashboardPage;
