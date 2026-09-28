import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Container, Row, Col, Card, Button, Badge } from 'react-bootstrap';
import { FaRocket, FaBrain, FaChartLine, FaComments, FaGraduationCap, FaLightbulb } from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';
import API from '../services/api';

const HomePage = () => {
  const { user, isAuthenticated } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await API.getQuestionStats();
        setStats(data);
      } catch (err) {
        setError('Failed to load statistics');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  const features = [
    {
      icon: <FaBrain size={40} />,
      title: 'AI-Powered Analysis',
      description: 'Get intelligent feedback on your interview responses using our multi-agent system.',
      color: '#667eea'
    },
    {
      icon: <FaComments size={40} />,
      title: 'Communication Coaching',
      description: 'Improve your clarity, structure, and overall communication quality.',
      color: '#f093fb'
    },
    {
      icon: <FaChartLine size={40} />,
      title: 'Progress Tracking',
      description: 'Track your improvement over time with detailed analytics and insights.',
      color: '#4facfe'
    },
    {
      icon: <FaGraduationCap size={40} />,
      title: 'Personalized Feedback',
      description: 'Receive tailored feedback based on your target role and experience level.',
      color: '#43e97b'
    },
    {
      icon: <FaLightbulb size={40} />,
      title: 'Multi-Agent System',
      description: 'Benefit from specialized agents for question selection, communication analysis, content evaluation, and STAR method assessment.',
      color: '#fa709a'
    },
    {
      icon: <FaRocket size={40} />,
      title: 'Practice Anywhere',
      description: 'Practice interview questions with text or voice responses, anytime, anywhere.',
      color: '#fee140'
    }
  ];

  const getStartedSteps = [
    {
      step: 1,
      title: 'Create Your Profile',
      description: 'Set up your candidate profile with your target role and experience.'
    },
    {
      step: 2,
      title: 'Start Practicing',
      description: 'Select a question category and start practicing interview questions.'
    },
    {
      step: 3,
      title: 'Get Feedback',
      description: 'Receive detailed, multi-agent analysis of your responses.'
    },
    {
      step: 4,
      title: 'Track Progress',
      description: 'Monitor your improvement and focus on areas that need work.'
    }
  ];

  if (loading) {
    return (
      <div className="spinner-container">
        <div className="loading-spinner"></div>
      </div>
    );
  }

  return (
    <div className="fade-in">
      {/* Hero Section */}
      <section className="page-header text-center">
        <h1>AI-Powered Interview Coaching</h1>
        <p className="lead">
          Master your interview skills with personalized, intelligent feedback
        </p>
        
        {isAuthenticated() ? (
          <div className="mt-4">
            <Link to="/practice">
              <Button variant="light" size="lg" className="me-3">
                Start Practicing
              </Button>
            </Link>
            <Link to="/dashboard">
              <Button variant="outline-light" size="lg">
                Go to Dashboard
              </Button>
            </Link>
          </div>
        ) : (
          <div className="mt-4">
            <Link to="/register">
              <Button variant="light" size="lg" className="me-3">
                Get Started Free
              </Button>
            </Link>
            <Link to="/login">
              <Button variant="outline-light" size="lg">
                Sign In
              </Button>
            </Link>
          </div>
        )}
      </section>

      {/* Features Section */}
      <section className="mb-5">
        <h2 className="section-title text-center">Why Choose Interview Coach?</h2>
        
        <Row className="g-4">
          {features.map((feature, index) => (
            <Col md={4} key={index}>
              <Card className="h-100 fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
                <Card.Body className="text-center">
                  <div 
                    className="d-inline-block p-3 mb-3"
                    style={{
                      background: `linear-gradient(135deg, ${feature.color} 0%, ${feature.color}dd 100%)`,
                      borderRadius: '15px'
                    }}
                  >
                    <span style={{ color: 'white', fontSize: '2rem' }}>
                      {feature.icon}
                    </span>
                  </div>
                  <Card.Title as="h4" className="mb-3">{feature.title}</Card.Title>
                  <Card.Text>
                    {feature.description}
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      </section>

      {/* Statistics Section */}
      {stats && (
        <section className="mb-5">
          <h2 className="section-title text-center">Interview Questions Database</h2>
          <Row className="g-4 text-center">
            <Col md={3}>
              <Card className="stat-card">
                <Card.Body>
                  <h3 className="display-6">{stats.by_role ? Object.keys(stats.by_role).length : 0}</h3>
                  <p>Different Roles</p>
                </Card.Body>
              </Card>
            </Col>
            <Col md={3}>
              <Card className="stat-card">
                <Card.Body>
                  <h3 className="display-6">{stats.by_competency ? Object.keys(stats.by_competency).length : 0}</h3>
                  <p>Competencies</p>
                </Card.Body>
              </Card>
            </Col>
            <Col md={3}>
              <Card className="stat-card">
                <Card.Body>
                  <h3 className="display-6">{stats.by_difficulty ? Object.values(stats.by_difficulty).reduce((a, b) => a + b, 0) : 0}</h3>
                  <p>Total Questions</p>
                </Card.Body>
              </Card>
            </Col>
            <Col md={3}>
              <Card className="stat-card">
                <Card.Body>
                  <h3 className="display-6">{stats.by_type ? Object.keys(stats.by_type).length : 0}</h3>
                  <p>Question Types</p>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </section>
      )}

      {/* How It Works Section */}
      <section className="mb-5">
        <h2 className="section-title text-center">How It Works</h2>
        
        <Row className="g-4">
          {getStartedSteps.map((step, index) => (
            <Col md={3} key={index}>
              <Card className="h-100">
                <Card.Body>
                  <Badge bg="primary" className="mb-3">Step {step.step}</Badge>
                  <Card.Title as="h5" className="mb-3">{step.title}</Card.Title>
                  <Card.Text>
                    {step.description}
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
      </section>

      {/* CTA Section */}
      <section className="text-center mb-5">
        <h2 className="section-title">Ready to Improve Your Interview Skills?</h2>
        
        {isAuthenticated() ? (
          <Link to="/practice">
            <Button variant="primary" size="lg" className="me-3">
              Start Practicing Now
            </Button>
          </Link>
        ) : (
          <>
            <Link to="/register">
              <Button variant="primary" size="lg" className="me-3">
                Sign Up Free
              </Button>
            </Link>
            <Link to="/login">
              <Button variant="outline-primary" size="lg">
                Sign In
              </Button>
            </Link>
          </>
        )}
      </section>
    </div>
  );
};

export default HomePage;
