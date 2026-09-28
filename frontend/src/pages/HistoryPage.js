import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Container, Row, Col, Card, Button, Badge, Table, Form, InputGroup, Alert, Spinner } from 'react-bootstrap';
import { 
  FaHistory, FaSearch, FaFilter, FaSort, FaEye, FaTrash, 
  FaChartBar, FaCalendar, FaClock, FaStar
} from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';
import API from '../services/api';
import toast from 'react-hot-toast';
import ReactMarkdown from 'react-markdown';

const HistoryPage = () => {
  const { user } = useAuth();
  const [candidate, setCandidate] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [feedbackList, setFeedbackList] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);
  const [selectedFeedback, setSelectedFeedback] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRole, setFilterRole] = useState('');
  const [filterType, setFilterType] = useState('');
  const [sortBy, setSortBy] = useState('date');
  const [sortOrder, setSortOrder] = useState('desc');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [pageSize] = useState(10);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Get candidate
        const candidateData = await API.getCurrentCandidate();
        setCandidate(candidateData);
        
        if (candidateData) {
          // Get feedback
          const feedbackData = await API.getFeedbackByCandidate(
            candidateData.id,
            { page, page_size: pageSize }
          );
          
          setFeedbackList(feedbackData.data || []);
          setTotal(feedbackData.total || 0);
        }
        
      } catch (err) {
        setError('Failed to load history');
        toast.error('Failed to load history');
      } finally {
        setLoading(false);
      }
    };

    if (user) {
      fetchData();
    }
  }, [user, page, pageSize]);

  // Filter and sort feedback
  const filteredFeedback = feedbackList
    .filter(item => {
      const matchesSearch = !searchTerm || 
        (item.question?.text && item.question.text.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (item.response?.text && item.response.text.toLowerCase().includes(searchTerm.toLowerCase()));
      
      const matchesRole = !filterRole || item.role === filterRole;
      const matchesType = !filterType || item.question_type === filterType;
      
      return matchesSearch && matchesRole && matchesType;
    })
    .sort((a, b) => {
      if (sortBy === 'date') {
        return sortOrder === 'desc' 
          ? new Date(b.created_at) - new Date(a.created_at)
          : new Date(a.created_at) - new Date(b.created_at);
      } else if (sortBy === 'score') {
        return sortOrder === 'desc'
          ? (b.overall_score || 0) - (a.overall_score || 0)
          : (a.overall_score || 0) - (b.overall_score || 0);
      }
      return 0;
    });

  // Get unique values for filters
  const roles = [...new Set(feedbackList.map(item => item.role).filter(Boolean))];
  const types = [...new Set(feedbackList.map(item => item.question_type).filter(Boolean))];

  // View feedback details
  const viewFeedback = (feedback) => {
    setSelectedFeedback(feedback);
  };

  // Close feedback view
  const closeFeedbackView = () => {
    setSelectedFeedback(null);
  };

  // Calculate score color
  const getScoreColor = (score) => {
    if (score >= 80) return 'success';
    if (score >= 60) return 'warning';
    return 'danger';
  };

  // Format date
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
  };

  // Pagination
  const totalPages = Math.ceil(total / pageSize);
  
  const goToPage = (pageNum) => {
    setPage(pageNum);
  };

  if (loading) {
    return (
      <Container fluid className="spinner-container py-5">
        <div className="loading-spinner"></div>
        <p className="mt-3">Loading your practice history...</p>
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
          <FaHistory className="me-3" />
          Practice History
        </h1>
        <p>
          Review your past interview practice sessions and feedback
        </p>
      </section>

      {/* Filters and Search */}
      <Card className="mb-4">
        <Card.Body>
          <Row className="g-3">
            <Col md={4}>
              <InputGroup>
                <InputGroup.Text>
                  <FaSearch />
                </InputGroup.Text>
                <Form.Control
                  type="text"
                  placeholder="Search questions or responses..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </InputGroup>
            </Col>
            
            <Col md={2}>
              <Form.Select
                value={filterRole}
                onChange={(e) => setFilterRole(e.target.value)}
              >
                <option value="">All Roles</option>
                {roles.map(role => (
                  <option key={role} value={role}>{role}</option>
                ))}
              </Form.Select>
            </Col>
            
            <Col md={2}>
              <Form.Select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
              >
                <option value="">All Types</option>
                {types.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </Form.Select>
            </Col>
            
            <Col md={2}>
              <Form.Select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
              >
                <option value="date">Sort by Date</option>
                <option value="score">Sort by Score</option>
              </Form.Select>
            </Col>
            
            <Col md={2}>
              <Form.Select
                value={sortOrder}
                onChange={(e) => setSortOrder(e.target.value)}
              >
                <option value="desc">Descending</option>
                <option value="asc">Ascending</option>
              </Form.Select>
            </Col>
          </Row>
        </Card.Body>
      </Card>

      {/* Results Summary */}
      {filteredFeedback.length > 0 && (
        <Alert variant="info" className="mb-4">
          <strong>{filteredFeedback.length}</strong> results found
          {searchTerm && ` for "${searchTerm}"`}
          {filterRole && ` (Role: ${filterRole})`}
          {filterType && ` (Type: ${filterType})`}
        </Alert>
      )}

      {/* History Table */}
      <Card className="mb-4">
        <Card.Header className="d-flex justify-content-between align-items-center">
          <span>
            <FaHistory className="me-2" />
            Your Practice Sessions
          </span>
          <Link to="/practice">
            <Button variant="primary" size="sm">
              <FaEye className="me-2" />
              Start New Session
            </Button>
          </Link>
        </Card.Header>
        
        <Card.Body className="p-0">
          {filteredFeedback.length === 0 ? (
            <Alert variant="warning" className="m-4">
              No practice sessions found. 
              <Link to="/practice">Start practicing now</Link> to see your history here.
            </Alert>
          ) : (
            <div className="table-responsive">
              <Table hover className="mb-0">
                <thead className="table-light">
                  <tr>
                    <th>#</th>
                    <th>Question</th>
                    <th>Type</th>
                    <th>Role</th>
                    <th>Score</th>
                    <th>Date</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredFeedback.slice(0, pageSize).map((item, index) => (
                    <tr key={index}>
                      <td>{(page - 1) * pageSize + index + 1}</td>
                      <td>
                        <div style={{ maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                          {item.question?.text || 'N/A'}
                        </div>
                      </td>
                      <td>
                        <Badge bg="info">
                          {item.question_type || 'N/A'}
                        </Badge>
                      </td>
                      <td>{item.role || 'N/A'}</td>
                      <td>
                        <Badge bg={getScoreColor(item.overall_score || 0)}>
                          {Math.round(item.overall_score || 0)}%
                        </Badge>
                      </td>
                      <td>
                        <small className="text-muted">
                          {formatDate(item.created_at)}
                        </small>
                      </td>
                      <td>
                        <Button
                          variant="outline-primary"
                          size="sm"
                          onClick={() => viewFeedback(item)}
                          title="View details"
                        >
                          <FaEye />
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </div>
          )}
        </Card.Body>
        
        {/* Pagination */}
        {totalPages > 1 && (
          <Card.Footer className="text-center">
            <div className="d-flex justify-content-center gap-2">
              <Button
                variant="outline-primary"
                size="sm"
                disabled={page === 1}
                onClick={() => goToPage(page - 1)}
              >
                Previous
              </Button>
              
              {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                const pageNum = Math.max(1, page - 2) + i;
                return (
                  <Button
                    key={pageNum}
                    variant={pageNum === page ? 'primary' : 'outline-primary'}
                    size="sm"
                    onClick={() => goToPage(pageNum)}
                  >
                    {pageNum}
                  </Button>
                );
              })}
              
              <Button
                variant="outline-primary"
                size="sm"
                disabled={page === totalPages}
                onClick={() => goToPage(page + 1)}
              >
                Next
              </Button>
            </div>
            <div className="mt-2">
              <small className="text-muted">
                Page {page} of {totalPages} ({total} total)
              </small>
            </div>
          </Card.Footer>
        )}
      </Card>

      {/* Feedback Details Modal */}
      {selectedFeedback && (
        <Card className="mb-4">
          <Card.Header className="d-flex justify-content-between align-items-center">
            <span>
              <FaEye className="me-2" />
              Feedback Details
            </span>
            <Button variant="outline-secondary" size="sm" onClick={closeFeedbackView}>
              Close
            </Button>
          </Card.Header>
          
          <Card.Body>
            {/* Question */}
            <div className="mb-4">
              <h5>
                <FaQuestionCircle className="me-2" />
                Question
              </h5>
              <Card className="bg-light">
                <Card.Body>
                  <p className="mb-1">{selectedFeedback.question?.text}</p>
                  <div className="text-muted small">
                    <Badge bg="info" className="me-2">
                      {selectedFeedback.question_type || 'N/A'}
                    </Badge>
                    <Badge bg="secondary">
                      {selectedFeedback.role || 'N/A'}
                    </Badge>
                  </div>
                </Card.Body>
              </Card>
            </div>

            {/* Response */}
            <div className="mb-4">
              <h5>
                <FaComments className="me-2" />
                Your Response
              </h5>
              <Card className="bg-light">
                <Card.Body>
                  <ReactMarkdown>{selectedFeedback.response?.text || 'No response text'}</ReactMarkdown>
                </Card.Body>
              </Card>
            </div>

            {/* Scores */}
            <div className="mb-4">
              <h5>
                <FaChartBar className="me-2" />
                Scores
              </h5>
              <Row className="g-3">
                <Col md={3}>
                  <Card className="text-center">
                    <Card.Body>
                      <h3 className="text-primary">{Math.round(selectedFeedback.overall_score || 0)}</h3>
                      <p className="mb-0">Overall</p>
                    </Card.Body>
                  </Card>
                </Col>
                <Col md={3}>
                  <Card className="text-center">
                    <Card.Body>
                      <h3 className="text-success">{Math.round(selectedFeedback.relevance_score || 0)}</h3>
                      <p className="mb-0">Relevance</p>
                    </Card.Body>
                  </Card>
                </Col>
                <Col md={3}>
                  <Card className="text-center">
                    <Card.Body>
                      <h3 className="text-info">{Math.round(selectedFeedback.clarity_score || 0)}</h3>
                      <p className="mb-0">Clarity</p>
                    </Card.Body>
                  </Card>
                </Col>
                <Col md={3}>
                  <Card className="text-center">
                    <Card.Body>
                      <h3 className="text-warning">{Math.round(selectedFeedback.structure_score || 0)}</h3>
                      <p className="mb-0">Structure</p>
                    </Card.Body>
                  </Card>
                </Col>
              </Row>
            </div>

            {/* Feedback */}
            <div className="mb-4">
              <h5>
                <FaStar className="me-2" />
                Feedback
              </h5>
              
              {selectedFeedback.strengths?.length > 0 && (
                <>
                  <h6 className="text-success mb-2">
                    <FaCheckCircle className="me-2" />
                    Strengths
                  </h6>
                  <ListGroup variant="flush" className="mb-3">
                    {selectedFeedback.strengths.map((strength, index) => (
                      <ListGroup.Item key={index}>{strength}</ListGroup.Item>
                    ))}
                  </ListGroup>
                </>
              )}

              {selectedFeedback.weaknesses?.length > 0 && (
                <>
                  <h6 className="text-danger mb-2">
                    <FaTimesCircle className="me-2" />
                    Areas for Improvement
                  </h6>
                  <ListGroup variant="flush" className="mb-3">
                    {selectedFeedback.weaknesses.map((weakness, index) => (
                      <ListGroup.Item key={index}>{weakness}</ListGroup.Item>
                    ))}
                  </ListGroup>
                </>
              )}

              {selectedFeedback.improvement_suggestions?.length > 0 && (
                <>
                  <h6 className="text-warning mb-2">
                    <FaLightbulb className="me-2" />
                    Suggestions
                  </h6>
                  <ListGroup variant="flush">
                    {selectedFeedback.improvement_suggestions.map((suggestion, index) => (
                      <ListGroup.Item key={index}>{suggestion}</ListGroup.Item>
                    ))}
                  </ListGroup>
                </>
              )}
            </div>

            {/* Additional Analysis */}
            {selectedFeedback.communication_analysis && (
              <div className="mb-4">
                <h5>
                  <FaComments className="me-2" />
                  Communication Analysis
                </h5>
                <Card className="bg-light">
                  <Card.Body>
                    <ReactMarkdown>{selectedFeedback.communication_analysis}</ReactMarkdown>
                  </Card.Body>
                </Card>
              </div>
            )}

            {selectedFeedback.star_analysis && (
              <div className="mb-4">
                <h5>
                  <FaStar className="me-2" />
                  STAR Analysis
                </h5>
                <Card className="bg-light">
                  <Card.Body>
                    <ReactMarkdown>{selectedFeedback.star_analysis}</ReactMarkdown>
                  </Card.Body>
                </Card>
              </div>
            )}

            {selectedFeedback.improved_response && (
              <div>
                <h5>
                  <FaStar className="me-2" />
                  Improved Response Example
                </h5>
                <Card className="bg-light">
                  <Card.Body>
                    <ReactMarkdown>{selectedFeedback.improved_response}</ReactMarkdown>
                  </Card.Body>
                </Card>
              </div>
            )}
          </Card.Body>
          
          <Card.Footer className="text-end">
            <small className="text-muted">
              Analyzed on: {formatDate(selectedFeedback.created_at)}
            </small>
          </Card.Footer>
        </Card>
      )}
    </div>
  );
};

export default HistoryPage;
