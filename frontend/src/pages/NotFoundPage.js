import React from 'react';
import { Link } from 'react-router-dom';
import { Container, Row, Col, Button } from 'react-bootstrap';
import { FaExclamationTriangle, FaHome, FaSearch } from 'react-icons/fa';

const NotFoundPage = () => {
  return (
    <Container fluid className="min-vh-100 d-flex align-items-center justify-content-center">
      <Row className="w-100">
        <Col md={8} className="mx-auto text-center">
          <div className="mb-4">
            <FaExclamationTriangle 
              className="text-warning" 
              style={{ fontSize: '6rem' }}
            />
          </div>
          
          <h1 className="display-4 mb-3">404 - Page Not Found</h1>
          <p className="lead mb-4">
            Oops! The page you're looking for doesn't exist or has been moved.
          </p>
          
          <div className="d-flex justify-content-center gap-3 flex-wrap">
            <Link to="/">
              <Button variant="primary" size="lg">
                <FaHome className="me-2" />
                Go to Home
              </Button>
            </Link>
            
            <Link to="/practice">
              <Button variant="outline-primary" size="lg">
                <FaSearch className="me-2" />
                Find Practice Questions
              </Button>
            </Link>
          </div>
          
          <div className="mt-5">
            <p className="text-muted">
              Need help? Contact our support team or check out our 
              <Link to="/">help center</Link>.
            </p>
          </div>
        </Col>
      </Row>
    </Container>
  );
};

export default NotFoundPage;
