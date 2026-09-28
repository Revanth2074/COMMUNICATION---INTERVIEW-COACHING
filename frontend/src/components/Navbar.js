import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Container, Nav, Navbar as BootstrapNavbar, NavDropdown, Button } from 'react-bootstrap';
import { FaHome, FaUser, FaChartLine, FaHistory, FaPlayCircle, FaSignInAlt, FaUserPlus } from 'react-icons/fa';

const Navbar = ({ user, onLogout }) => {
  const location = useLocation();
  const [expanded, setExpanded] = useState(false);

  const handleLogout = () => {
    setExpanded(false);
    onLogout();
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <BootstrapNavbar 
      expand="lg" 
      className="navbar-custom mb-4"
      expanded={expanded}
      onToggle={() => setExpanded(!expanded)}
    >
      <Container fluid>
        <BootstrapNavbar.Brand as={Link} to="/" className="d-flex align-items-center">
          <span className="me-2">
            <FaPlayCircle size={24} />
          </span>
          Interview Coach
        </BootstrapNavbar.Brand>
        
        <BootstrapNavbar.Toggle aria-controls="basic-navbar-nav" />
        
        <BootstrapNavbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link 
              as={Link} 
              to="/" 
              className={isActive('/') ? 'active' : ''}
              onClick={() => setExpanded(false)}
            >
              <FaHome className="me-1" />
              Home
            </Nav.Link>
            
            {user && (
              <>
                <Nav.Link 
                  as={Link} 
                  to="/dashboard" 
                  className={isActive('/dashboard') ? 'active' : ''}
                  onClick={() => setExpanded(false)}
                >
                  <FaChartLine className="me-1" />
                  Dashboard
                </Nav.Link>
                
                <Nav.Link 
                  as={Link} 
                  to="/practice" 
                  className={isActive('/practice') ? 'active' : ''}
                  onClick={() => setExpanded(false)}
                >
                  <FaPlayCircle className="me-1" />
                  Practice
                </Nav.Link>
                
                <Nav.Link 
                  as={Link} 
                  to="/history" 
                  className={isActive('/history') ? 'active' : ''}
                  onClick={() => setExpanded(false)}
                >
                  <FaHistory className="me-1" />
                  History
                </Nav.Link>
                
                <Nav.Link 
                  as={Link} 
                  to="/progress" 
                  className={isActive('/progress') ? 'active' : ''}
                  onClick={() => setExpanded(false)}
                >
                  <FaChartLine className="me-1" />
                  Progress
                </Nav.Link>
              </>
            )}
          </Nav>
          
          <Nav>
            {user ? (
              <>
                <NavDropdown 
                  title={
                    <>
                      <FaUser className="me-1" />
                      {user.username}
                    </>
                  }
                  id="basic-nav-dropdown"
                  align="end"
                >
                  <NavDropdown.Item as={Link} to="/profile" onClick={() => setExpanded(false)}>
                    <FaUser className="me-2" />
                    Profile
                  </NavDropdown.Item>
                  <NavDropdown.Divider />
                  <NavDropdown.Item onClick={handleLogout}>
                    <FaSignInAlt className="me-2" />
                    Logout
                  </NavDropdown.Item>
                </NavDropdown>
              </>
            ) : (
              <>
                <Button 
                  variant="outline-light" 
                  as={Link} 
                  to="/login" 
                  className="me-2"
                  onClick={() => setExpanded(false)}
                >
                  <FaSignInAlt className="me-1" />
                  Login
                </Button>
                <Button 
                  variant="light" 
                  as={Link} 
                  to="/register" 
                  onClick={() => setExpanded(false)}
                >
                  <FaUserPlus className="me-1" />
                  Register
                </Button>
              </>
            )}
          </Nav>
        </BootstrapNavbar.Collapse>
      </Container>
    </BootstrapNavbar>
  );
};

export default Navbar;
