import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { Container, Row, Col, Card, Button, Form, Badge, ProgressBar, Alert, Spinner, Modal, ListGroup } from 'react-bootstrap';
import { 
  FaPlayCircle, FaMicrophone, FaStop, FaVolumeUp, FaArrowRight, 
  FaBrain, FaComments, FaStar, FaCheckCircle, FaTimesCircle,
  FaLightbulb, FaQuestionCircle, FaStepBackward, FaStepForward
} from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';
import API from '../services/api';
import toast from 'react-hot-toast';

const PracticePage = () => {
  const { user } = useAuth();
  const [candidate, setCandidate] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [responseText, setResponseText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const [showSTARExample, setShowSTARExample] = useState(false);
  const [starExample, setSTARExample] = useState('');
  
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  useEffect(() => {
    const fetchCandidate = async () => {
      try {
        const data = await API.getCurrentCandidate();
        setCandidate(data);
      } catch (err) {
        toast.error('Failed to load candidate profile');
      }
    };

    if (user) {
      fetchCandidate();
    }
  }, [user]);

  // Fetch a new question
  const fetchQuestion = async () => {
    setLoading(true);
    try {
      // Use multi-agent system to get a question
      const result = await API.startPracticeSession({
        candidate_id: candidate?.id || 0,
        target_role: candidate?.target_role,
        difficulty: 'medium'
      });
      
      if (result.success && result.data.question) {
        setCurrentQuestion(result.data.question);
        setSessionId(result.data.session?.id || null);
        setResponseText('');
        setAnalysis(null);
        setShowFeedback(false);
      } else {
        // Fallback: get random question from database
        const question = await API.getRandomQuestion({
          role: candidate?.target_role
        });
        setCurrentQuestion(question);
      }
    } catch (err) {
      toast.error('Failed to load question');
      // Fallback to a default question
      setCurrentQuestion({
        id: 0,
        text: 'Tell me about yourself and your experience.',
        role: 'General',
        competency: 'Communication',
        difficulty: 'easy',
        question_type: 'behavioral'
      });
    } finally {
      setLoading(false);
    }
  };

  // Initialize with a question
  useEffect(() => {
    if (candidate) {
      fetchQuestion();
    }
  }, [candidate]);

  // Start recording
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];
      
      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };
      
      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);
        
        // In a real implementation, we would upload this to the server
        // For now, we'll just transcribe it locally (mock)
        try {
          const result = await API.transcribeAudio(audioBlob);
          if (result.success) {
            setResponseText(result.data.transcription);
          }
        } catch (err) {
          toast.warning('Audio transcription not available. Please type your response.');
        }
        
        // Clean up
        stream.getTracks().forEach(track => track.stop());
      };
      
      mediaRecorderRef.current.start();
      setIsRecording(true);
      toast.success('Recording started');
      
    } catch (err) {
      toast.error('Could not start recording. Please check microphone permissions.');
    }
  };

  // Stop recording
  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      toast.success('Recording stopped');
    }
  };

  // Submit response for analysis
  const submitResponse = async () => {
    if (!responseText.trim()) {
      toast.error('Please enter a response before submitting');
      return;
    }

    setSubmitting(true);
    setAnalysis(null);
    
    try {
      // Use multi-agent system to analyze the response
      const result = await API.analyzePracticeResponse({
        candidate_id: candidate?.id || 0,
        question_id: currentQuestion?.id || 0,
        session_id: sessionId || 0,
        response_text: responseText,
        response_type: 'text'
      });
      
      if (result.success) {
        setAnalysis(result.data);
        setShowFeedback(true);
        
        // Add to history
        setHistory(prev => [
          ...prev,
          {
            question: currentQuestion,
            response: responseText,
            analysis: result.data,
            timestamp: new Date().toISOString()
          }
        ]);
      } else {
        toast.error('Failed to analyze response');
      }
    } catch (err) {
      toast.error('Failed to analyze response');
    } finally {
      setSubmitting(false);
    }
  };

  // Quick analyze without saving
  const quickAnalyze = async () => {
    if (!responseText.trim()) {
      toast.error('Please enter a response before analyzing');
      return;
    }

    setSubmitting(true);
    
    try {
      const result = await API.quickAnalyzeResponse(
        responseText,
        currentQuestion?.text || 'Unknown question'
      );
      
      if (result.success) {
        setAnalysis(result.data);
        setShowFeedback(true);
      }
    } catch (err) {
      toast.error('Failed to analyze response');
    } finally {
      setSubmitting(false);
    }
  };

  // Get STAR example
  const getSTARExample = async () => {
    try {
      const result = await API.generateSTARExample(currentQuestion?.text || '');
      if (result.success) {
        setSTARExample(result.data.response || 'No example available');
        setShowSTARExample(true);
      }
    } catch (err) {
      toast.error('Failed to generate STAR example');
    }
  };

  // Get next question
  const nextQuestion = () => {
    fetchQuestion();
    setShowFeedback(false);
  };

  // Get follow-up question
  const getFollowUp = async () => {
    if (!currentQuestion || !responseText.trim()) {
      toast.error('Please answer the current question first');
      return;
    }

    try {
      const result = await API.getFollowUpQuestion({
        candidate_id: candidate?.id || 0,
        previous_question_id: currentQuestion.id || 0,
        previous_response: responseText
      });
      
      if (result.success && result.data.question) {
        setCurrentQuestion({
          ...currentQuestion,
          text: result.data.question.text,
          type: 'follow_up'
        });
        setResponseText('');
        setShowFeedback(false);
        toast.success('Follow-up question loaded');
      }
    } catch (err) {
      toast.error('Failed to generate follow-up question');
    }
  };

  // Calculate score color
  const getScoreColor = (score) => {
    if (score >= 80) return 'success';
    if (score >= 60) return 'warning';
    return 'danger';
  };

  if (loading && !currentQuestion) {
    return (
      <Container fluid className="spinner-container py-5">
        <div className="loading-spinner"></div>
        <p className="mt-3">Loading your first question...</p>
      </Container>
    );
  }

  return (
    <div className="fade-in">
      {/* Header */}
      <section className="page-header">
        <h1>
          <FaPlayCircle className="me-3" />
          Practice Interview Questions
        </h1>
        <p>
          Answer questions and receive intelligent feedback from our multi-agent system
        </p>
      </section>

      <Row className="g-4">
        {/* Question Card */}
        <Col lg={6}>
          <Card className="question-card">
            <Card.Header className="d-flex justify-content-between align-items-center">
              <div>
                <Badge bg="primary" className="me-2">
                  {currentQuestion?.difficulty || 'medium'}
                </Badge>
                <Badge bg="info">
                  {currentQuestion?.question_type || 'general'}
                </Badge>
              </div>
              <Button 
                variant="outline-light" 
                size="sm" 
                onClick={getSTARExample}
                title="Get STAR example"
              >
                <FaLightbulb />
              </Button>
            </Card.Header>
            
            <Card.Body>
              <h4 className="mb-3">{currentQuestion?.text || 'Loading question...'}</h4>
              
              <div className="question-meta text-muted small">
                <span className="me-3">
                  <strong>Role:</strong> {currentQuestion?.role || 'General'}
                </span>
                <span>
                  <strong>Competency:</strong> {currentQuestion?.competency || 'General'}
                </span>
              </div>
            </Card.Body>
            
            <Card.Footer className="text-end">
              <Button 
                variant="outline-primary" 
                size="sm" 
                onClick={getFollowUp}
                disabled={!responseText.trim()}
                className="me-2"
              >
                <FaQuestionCircle className="me-1" />
                Follow-up
              </Button>
              <Button 
                variant="outline-secondary" 
                size="sm" 
                onClick={nextQuestion}
              >
                <FaStepForward className="me-1" />
                Next Question
              </Button>
            </Card.Footer>
          </Card>

          {/* Response Input */}
          <Card className="mt-4">
            <Card.Header>
              <FaComments className="me-2" />
              Your Response
            </Card.Header>
            <Card.Body>
              <Form.Group>
                <Form.Control
                  as="textarea"
                  rows={6}
                  value={responseText}
                  onChange={(e) => setResponseText(e.target.value)}
                  placeholder="Type your answer here..."
                  className="response-area"
                  disabled={isRecording}
                />
              </Form.Group>
              
              <div className="d-flex justify-content-between align-items-center mt-3">
                <div>
                  {isRecording ? (
                    <Button 
                      variant="danger" 
                      onClick={stopRecording}
                    >
                      <FaStop className="me-2" />
                      Stop Recording
                    </Button>
                  ) : (
                    <Button 
                      variant="primary" 
                      onClick={startRecording}
                      disabled={!navigator.mediaDevices}
                    >
                      <FaMicrophone className="me-2" />
                      Record Voice
                    </Button>
                  )}
                </div>
                
                <div>
                  <Button 
                    variant="success" 
                    onClick={submitResponse}
                    disabled={submitting || !responseText.trim()}
                    className="me-2"
                  >
                    {submitting ? (
                      <>
                        <Spinner animation="border" size="sm" className="me-2" />
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <FaBrain className="me-2" />
                        Get Full Analysis
                      </>
                    )}
                  </Button>
                  
                  <Button 
                    variant="outline-success" 
                    onClick={quickAnalyze}
                    disabled={submitting || !responseText.trim()}
                  >
                    <FaArrowRight className="me-2" />
                    Quick Feedback
                  </Button>
                </div>
              </div>
            </Card.Body>
          </Card>
        </Col>

        {/* Feedback Card */}
        <Col lg={6}>
          {showFeedback && analysis ? (
            <Card className="feedback-card">
              <Card.Header className="d-flex justify-content-between align-items-center">
                <span>
                  <FaBrain className="me-2" />
                  Multi-Agent Analysis
                </span>
                <Badge bg="light" text="dark">
                  Score: {Math.round(analysis.overall_score || 0)}/100
                </Badge>
              </Card.Header>
              
              <Card.Body>
                {/* Overall Score */}
                <div className="text-center mb-4">
                  <div className="score-circle mx-auto">
                    {Math.round(analysis.overall_score || 0)}
                  </div>
                  <div className="score-label">
                    Overall Score
                  </div>
                  <ProgressBar 
                    now={analysis.overall_score || 0} 
                    max={100}
                    variant={getScoreColor(analysis.overall_score || 0)}
                    className="mt-2"
                  />
                </div>

                {/* Performance Summary */}
                <div className="mb-4">
                  <h5 className="mb-3">
                    <FaComments className="me-2" />
                    Performance Summary
                  </h5>
                  <p>{analysis.performance_summary || 'Analysis in progress...'}</p>
                </div>

                {/* Agent Scores */}
                <h5 className="mb-3">
                  <FaBrain className="me-2" />
                  Agent Scores
                </h5>
                <Row className="g-2 mb-4">
                  <Col xs={6}>
                    <div className="d-flex align-items-center mb-2">
                      <span className="me-2">Communication:</span>
                      <Badge bg={getScoreColor(analysis.agent_feedback_summary?.communication?.score || 0)}>
                        {Math.round(analysis.agent_feedback_summary?.communication?.score || 0)}
                      </Badge>
                    </div>
                  </Col>
                  <Col xs={6}>
                    <div className="d-flex align-items-center mb-2">
                      <span className="me-2">Content:</span>
                      <Badge bg={getScoreColor(analysis.agent_feedback_summary?.content?.score || 0)}>
                        {Math.round(analysis.agent_feedback_summary?.content?.score || 0)}
                      </Badge>
                    </div>
                  </Col>
                  <Col xs={6}>
                    <div className="d-flex align-items-center mb-2">
                      <span className="me-2">Structure:</span>
                      <Badge bg={getScoreColor(analysis.agent_feedback_summary?.star?.score || 0)}>
                        {Math.round(analysis.agent_feedback_summary?.star?.score || 0)}
                      </Badge>
                    </div>
                  </Col>
                  <Col xs={6}>
                    <div className="d-flex align-items-center mb-2">
                      <span className="me-2">Relevance:</span>
                      <Badge bg={getScoreColor(analysis.detailed_scores?.content?.relevance_score || 0)}>
                        {Math.round(analysis.detailed_scores?.content?.relevance_score || 0)}
                      </Badge>
                    </div>
                  </Col>
                </Row>

                {/* Strengths */}
                <h5 className="mb-3">
                  <FaCheckCircle className="me-2 text-success" />
                  Strengths
                </h5>
                <ListGroup variant="flush" className="mb-4">
                  {analysis.agent_feedback_summary?.communication?.strengths?.map((strength, index) => (
                    <ListGroup.Item key={index} className="small">
                      {strength}
                    </ListGroup.Item>
                  ))}
                  {analysis.agent_feedback_summary?.content?.strengths?.map((strength, index) => (
                    <ListGroup.Item key={index} className="small">
                      {strength}
                    </ListGroup.Item>
                  ))}
                  {analysis.agent_feedback_summary?.star?.strengths?.map((strength, index) => (
                    <ListGroup.Item key={index} className="small">
                      {strength}
                    </ListGroup.Item>
                  ))}
                </ListGroup>

                {/* Improvement Suggestions */}
                <h5 className="mb-3">
                  <FaLightbulb className="me-2 text-warning" />
                  Improvement Suggestions
                </h5>
                <ListGroup variant="flush">
                  {analysis.personalized_recommendations?.map((rec, index) => (
                    <ListGroup.Item key={index} className="small">
                      <strong>{rec.area}:</strong> {rec.action}
                    </ListGroup.Item>
                  ))}
                  {analysis.improvement_plan?.short_term?.map((item, index) => (
                    <ListGroup.Item key={index} className="small">
                      {item}
                    </ListGroup.Item>
                  ))}
                </ListGroup>

                {analysis.improved_response_example && (
                  <>
                    <h5 className="mt-4 mb-3">
                      <FaStar className="me-2" />
                      Example Improved Response
                    </h5>
                    <Card className="bg-light">
                      <Card.Body>
                        <p className="small">{analysis.improved_response_example}</p>
                      </Card.Body>
                    </Card>
                  </>
                )}

                {analysis.follow_up_questions?.length > 0 && (
                  <>
                    <h5 className="mt-4 mb-3">
                      <FaQuestionCircle className="me-2" />
                      Suggested Follow-up Questions
                    </h5>
                    <ListGroup variant="flush">
                      {analysis.follow_up_questions.map((question, index) => (
                        <ListGroup.Item key={index} className="small">
                          {question}
                        </ListGroup.Item>
                      ))}
                    </ListGroup>
                  </>
                )}
              </Card.Body>
              
              <Card.Footer className="text-center">
                <Button variant="primary" onClick={nextQuestion}>
                  <FaStepForward className="me-2" />
                  Next Question
                </Button>
              </Card.Footer>
            </Card>
          ) : (
            <Card className="text-center">
              <Card.Body>
                <FaBrain className="display-4 text-primary mb-3" />
                <h4>Ready for Analysis?</h4>
                <p className="text-muted">
                  Type or record your response, then click "Get Full Analysis" to receive 
                  comprehensive feedback from our multi-agent system.
                </p>
              </Card.Body>
            </Card>
          )}
        </Col>
      </Row>

      {/* STAR Example Modal */}
      <Modal show={showSTARExample} onHide={() => setShowSTARExample(false)} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>
            <FaStar className="me-2" />
            STAR Method Example
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Card className="mb-4">
            <Card.Header>
              <strong>Question:</strong> {currentQuestion?.text}
            </Card.Header>
            <Card.Body>
              <h5>STAR Response Example:</h5>
              <p className="mt-3">{starExample || 'Loading example...'}</p>
            </Card.Body>
          </Card>
          
          <Alert variant="info">
            <strong>STAR Method:</strong> Situation, Task, Action, Result
          </Alert>
          
          <h6>How to use STAR:</h6>
          <ListGroup variant="flush">
            <ListGroup.Item>
              <strong>Situation:</strong> Describe the context and background
            </ListGroup.Item>
            <ListGroup.Item>
              <strong>Task:</strong> Explain your responsibility or goal
            </ListGroup.Item>
            <ListGroup.Item>
              <strong>Action:</strong> Detail what you did (focus on your actions)
            </ListGroup.Item>
            <ListGroup.Item>
              <strong>Result:</strong> Share the outcome and impact
            </ListGroup.Item>
          </ListGroup>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowSTARExample(false)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>

      {/* History Modal */}
      <Modal show={showHistory} onHide={() => setShowHistory(false)} size="xl">
        <Modal.Header closeButton>
          <Modal.Title>Practice History</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {history.length === 0 ? (
            <Alert variant="info">No practice history yet. Start answering questions!</Alert>
          ) : (
            <ListGroup variant="flush">
              {history.map((item, index) => (
                <ListGroup.Item key={index} className="mb-3">
                  <div className="d-flex justify-content-between align-items-start">
                    <div>
                      <h6>Question {index + 1}:</h6>
                      <p className="mb-1">{item.question?.text}</p>
                      <small className="text-muted">
                        {new Date(item.timestamp).toLocaleString()}
                      </small>
                    </div>
                    <Badge bg="primary">
                      {Math.round(item.analysis?.overall_score || 0)}%
                    </Badge>
                  </div>
                  <hr />
                </ListGroup.Item>
              ))}
            </ListGroup>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowHistory(false)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default PracticePage;
