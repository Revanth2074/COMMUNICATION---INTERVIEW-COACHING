import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Container, Row, Col, Card, Button, Badge, ProgressBar, Alert, Spinner } from 'react-bootstrap';
import { 
  FaChartLine, FaArrowUp, FaArrowDown, FaTrophy, FaFire, 
  FaBrain, FaComments, FaStar, FaHistory, FaLightbulb,
  FaCalendar, FaClock, FaChartBar, FaList
} from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';
import API from '../services/api';
import toast from 'react-hot-toast';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const ProgressPage = () => {
  const { user } = useAuth();
  const [candidate, setCandidate] = useState(null);
  const [progressSummary, setProgressSummary] = useState(null);
  const [progressList, setProgressList] = useState([]);
  const [improvementAreas, setImprovementAreas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [timeRange, setTimeRange] = useState('all');

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Get candidate
        const candidateData = await API.getCurrentCandidate();
        setCandidate(candidateData);
        
        if (candidateData) {
          // Get progress summary
          const summary = await API.getProgressSummary(candidateData.id);
          setProgressSummary(summary);
          
          // Get progress list
          const progress = await API.getProgressByCandidate(candidateData.id, { page_size: 50 });
          setProgressList(progress.data || []);
          
          // Get improvement areas
          const improvements = await API.getImprovementAreas(candidateData.id);
          setImprovementAreas(improvements);
        }
        
      } catch (err) {
        setError('Failed to load progress data');
        toast.error('Failed to load progress data');
      } finally {
        setLoading(false);
      }
    };

    if (user) {
      fetchData();
    }
  }, [user]);

  // Calculate chart data
  const getScoreChartData = () => {
    if (!progressSummary || !progressSummary.by_area) return [];
    
    return Object.entries(progressSummary.by_area).map(([area, data]) => ({
      name: area,
      score: Math.round(data.average || 0)
    }));
  };

  const getCompetencyChartData = () => {
    if (!progressSummary || !progressSummary.by_competency) return [];
    
    return Object.entries(progressSummary.by_competency).map(([competency, data]) => ({
      name: competency,
      score: Math.round(data.average || 0)
    }));
  };

  const getRecentTrendData = () => {
    if (!progressSummary || !progressSummary.recent_trend) return [];
    
    return progressSummary.recent_trend.map((item, index) => ({
      name: `Session ${index + 1}`,
      score: Math.round(item.score || 0)
    }));
  };

  // Colors for charts
  const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a', '#fee140'];

  // Calculate score color
  const getScoreColor = (score) => {
    if (score >= 80) return 'success';
    if (score >= 60) return 'warning';
    return 'danger';
  };

  // Calculate improvement percentage
  const calculateImprovement = (baseline, current) => {
    if (baseline === 0) return 0;
    return Math.round(((current - baseline) / baseline) * 100);
  };

  // Format date
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) {
    return (
      <Container fluid className="spinner-container py-5">
        <div className="loading-spinner"></div>
        <p className="mt-3">Loading your progress data...</p>
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
          <FaChartLine className="me-3" />
          Your Progress
        </h1>
        <p>
          Track your improvement and identify areas for growth
        </p>
      </section>

      {/* Summary Cards */}
      {progressSummary && (
        <section className="mb-5">
          <h2 className="section-title">Overall Performance</h2>
          <Row className="g-4">
            <Col md={3}>
              <Card className="stat-card">
                <Card.Body className="text-center">
                  <div className="score-circle mx-auto mb-3">
                    {Math.round(progressSummary.overall.average_score || 0)}
                  </div>
                  <h5>Overall Score</h5>
                  <p className="text-muted small">
                    Average across all sessions
                  </p>
                  <ProgressBar 
                    now={progressSummary.overall.average_score || 0} 
                    max={100}
                    variant={getScoreColor(progressSummary.overall.average_score || 0)}
                    className="mt-2"
                  />
                </Card.Body>
              </Card>
            </Col>
            
            <Col md={3}>
              <Card className="stat-card">
                <Card.Body className="text-center">
                  <FaTrophy className="display-6 text-primary mb-3" />
                  <h5>{progressSummary.overall.total_sessions || 0}</h5>
                  <p className="mb-0">Practice Sessions</p>
                  <small className="text-muted">Completed</small>
                </Card.Body>
              </Card>
            </Col>
            
            <Col md={3}>
              <Card className="stat-card">
                <Card.Body className="text-center">
                  <FaFire className="display-6 text-warning mb-3" />
                  <h5>{Math.round(progressSummary.overall.average_score || 0)}%</h5>
                  <p className="mb-0">Average Score</p>
                  <small className="text-muted">Across all areas</small>
                </Card.Body>
              </Card>
            </Col>
            
            <Col md={3}>
              <Card className="stat-card">
                <Card.Body className="text-center">
                  <FaChartLine className="display-6 text-success mb-3" />
                  <h5>
                    {progressSummary.overall.improvement_trend === 'stable' ? 'Stable' : 
                     progressSummary.overall.improvement_trend === 'improving' ? 'Improving' : 'Needs Work'}
                  </h5>
                  <p className="mb-0">Performance Trend</p>
                  <small className="text-muted">Overall direction</small>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </section>
      )}

      {/* Charts */}
      {progressSummary && (
        <section className="mb-5">
          <h2 className="section-title">Performance Analytics</h2>
          
          <Row className="g-4 mb-4">
            {/* Score by Area Chart */}
            <Col md={6}>
              <Card className="chart-container">
                <Card.Header>
                  <FaBrain className="me-2" />
                  Score by Assessment Area
                </Card.Header>
                <Card.Body>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={getScoreChartData()}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="score" fill="#667eea" name="Score" />
                    </BarChart>
                  </ResponsiveContainer>
                </Card.Body>
              </Card>
            </Col>
            
            {/* Score by Competency Chart */}
            <Col md={6}>
              <Card className="chart-container">
                <Card.Header>
                  <FaTrophy className="me-2" />
                  Score by Competency
                </Card.Header>
                <Card.Body>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={getCompetencyChartData()}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="score"
                        nameKey="name"
                        label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      >
                        {getCompetencyChartData().map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </Card.Body>
              </Card>
            </Col>
          </Row>

          {/* Recent Trend Chart */}
          <Row className="g-4">
            <Col md={12}>
              <Card className="chart-container">
                <Card.Header>
                  <FaChartBar className="me-2" />
                  Recent Performance Trend
                </Card.Header>
                <Card.Body>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={getRecentTrendData()}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line 
                        type="monotone" 
                        dataKey="score" 
                        stroke="#667eea" 
                        strokeWidth={3}
                        name="Score"
                        activeDot={{ r: 8 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </section>
      )}

      {/* Detailed Progress */}
      {progressList.length > 0 && (
        <section className="mb-5">
          <h2 className="section-title">Detailed Progress</h2>
          
          <Card className="mb-4">
            <Card.Header className="d-flex justify-content-between align-items-center">
              <span>
                <FaList className="me-2" />
                Progress Over Time
              </span>
              <Link to="/history">
                <Button variant="outline-primary" size="sm">
                  <FaHistory className="me-2" />
                  View Full History
                </Button>
              </Link>
            </Card.Header>
            <Card.Body>
              <div className="table-responsive">
                <table className="table table-hover">
                  <thead className="table-light">
                    <tr>
                      <th>#</th>
                      <th>Competency</th>
                      <th>Area</th>
                      <th>Baseline</th>
                      <th>Current</th>
                      <th>Improvement</th>
                      <th>Last Updated</th>
                    </tr>
                  </thead>
                  <tbody>
                    {progressList
                      .sort((a, b) => new Date(b.last_updated) - new Date(a.last_updated))
                      .slice(0, 10)
                      .map((item, index) => {
                        const improvement = calculateImprovement(item.baseline_score, item.current_score);
                        return (
                          <tr key={index}>
                            <td>{index + 1}</td>
                            <td>
                              <Badge bg="info">{item.competency}</Badge>
                            </td>
                            <td>{item.area}</td>
                            <td>{Math.round(item.baseline_score)}</td>
                            <td>{Math.round(item.current_score)}</td>
                            <td>
                              <Badge 
                                bg={improvement > 0 ? 'success' : improvement < 0 ? 'danger' : 'secondary'}
                              >
                                {improvement > 0 ? '+' : ''}{improvement}%
                              </Badge>
                            </td>
                            <td>
                              <small className="text-muted">
                                {formatDate(item.last_updated)}
                              </small>
                            </td>
                          </tr>
                        );
                      })}
                  </tbody>
                </table>
              </div>
            </Card.Body>
          </Card>
        </section>
      )}

      {/* Improvement Areas */}
      {improvementAreas.length > 0 ? (
        <section className="mb-5">
          <h2 className="section-title">Areas for Improvement</h2>
          
          <Alert variant="warning" className="mb-4">
            <FaLightbulb className="me-2" />
            Focus on these areas to improve your interview performance
          </Alert>
          
          <Row className="g-4">
            {improvementAreas.map((area, index) => (
              <Col md={4} key={index}>
                <Card className="improvement-item border-warning">
                  <Card.Body>
                    <div className="d-flex justify-content-between align-items-start mb-3">
                      <div>
                        <h5 className="mb-1">{area.name}</h5>
                        <Badge bg={area.type === 'area' ? 'warning' : 'primary'}>
                          {area.type}
                        </Badge>
                      </div>
                      <Badge bg="danger" className="p-2">
                        -{Math.round(area.deficit)} pts
                      </Badge>
                    </div>
                    
                    <div className="mb-3">
                      <div className="d-flex align-items-center mb-2">
                        <ProgressBar 
                          now={area.current_score} 
                          max={100}
                          variant="warning"
                          className="flex-grow-1 me-2"
                        />
                        <span>{Math.round(area.current_score)}/100</span>
                      </div>
                    </div>
                    
                    <p className="mb-0 text-muted small">
                      Current score is {Math.round(area.current_score)}. 
                      Aim for {Math.round(area.current_score + area.deficit)} to reach the threshold.
                    </p>
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        </section>
      ) : (
        <section className="mb-5">
          <Alert variant="success" className="text-center">
            <FaTrophy className="me-2" />
            <strong>Great job!</strong> You're performing well across all areas. 
            Keep practicing to maintain your high scores!
          </Alert>
        </section>
      )}

      {/* Tips Section */}
      <section className="mb-5">
        <h2 className="section-title">Personalized Recommendations</h2>
        
        <Row className="g-4">
          <Col md={4}>
            <Card className="h-100">
              <Card.Body>
                <div className="d-flex align-items-center mb-3">
                  <FaBrain className="me-3" style={{ color: '#667eea', fontSize: '1.5rem' }} />
                  <Card.Title as="h6" className="mb-0">Practice Regularly</Card.Title>
                </div>
                <Card.Text>
                  Consistent practice with our AI-powered system will help you improve 
                  your interview skills significantly over time.
                </Card.Text>
                <Link to="/practice">
                  <Button variant="outline-primary" size="sm">
                    Start Practicing
                  </Button>
                </Link>
              </Card.Body>
            </Card>
          </Col>
          
          <Col md={4}>
            <Card className="h-100">
              <Card.Body>
                <div className="d-flex align-items-center mb-3">
                  <FaStar className="me-3" style={{ color: '#f093fb', fontSize: '1.5rem' }} />
                  <Card.Title as="h6" className="mb-0">Focus on Weak Areas</Card.Title>
                </div>
                <Card.Text>
                  Use the improvement areas identified above to focus your practice 
                  on the skills that need the most work.
                </Card.Text>
                {improvementAreas.length > 0 && (
                  <Link to="/practice">
                    <Button variant="outline-primary" size="sm">
                      Target Practice
                    </Button>
                  </Link>
                )}
              </Card.Body>
            </Card>
          </Col>
          
          <Col md={4}>
            <Card className="h-100">
              <Card.Body>
                <div className="d-flex align-items-center mb-3">
                  <FaChartLine className="me-3" style={{ color: '#43e97b', fontSize: '1.5rem' }} />
                  <Card.Title as="h6" className="mb-0">Track Your Progress</Card.Title>
                </div>
                <Card.Text>
                  Regularly review your progress to see how you're improving and 
                  celebrate your achievements.
                </Card.Text>
                <Link to="/history">
                  <Button variant="outline-primary" size="sm">
                    View History
                  </Button>
                </Link>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </section>
    </div>
  );
};

export default ProgressPage;
