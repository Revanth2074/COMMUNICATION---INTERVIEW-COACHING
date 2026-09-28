import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { FaGithub, FaLinkedin, FaEnvelope, FaHeart } from 'react-icons/fa';

const Footer = () => {
  return (
    <footer className="mt-5 py-4 bg-white rounded-top">
      <Container fluid>
        <Row className="align-items-center">
          <Col md={6} className="text-center text-md-start mb-3 mb-md-0">
            <p className="mb-0">
              <strong>Interview Coach</strong> - AI-Powered Communication & Interview Coaching System
            </p>
            <p className="mb-0 text-muted small">
              Helping candidates improve their interview skills with personalized feedback
            </p>
          </Col>
          
          <Col md={6} className="text-center text-md-end">
            <div className="d-flex justify-content-center justify-content-md-end gap-3">
              <a 
                href="https://github.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-muted"
                title="GitHub"
              >
                <FaGithub size={20} />
              </a>
              <a 
                href="https://linkedin.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-muted"
                title="LinkedIn"
              >
                <FaLinkedin size={20} />
              </a>
              <a 
                href="mailto:contact@interviewcoach.com" 
                className="text-muted"
                title="Email"
              >
                <FaEnvelope size={20} />
              </a>
            </div>
            <p className="mb-0 text-muted small mt-2">
              Made with <FaHeart className="text-danger" /> for better interviews
            </p>
          </Col>
        </Row>
        
        <Row className="mt-3 pt-3 border-top">
          <Col className="text-center text-muted small">
            &copy; {new Date().getFullYear()} Interview Coach. All rights reserved.
          </Col>
        </Row>
      </Container>
    </footer>
  );
};

export default Footer;
