import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';

import useAuth from '../hooks/index.js';
import { useNavigate } from "react-router-dom";


const NavbarPage = () => {
  const auth = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('user');
    auth.loggedIn = false;
    return navigate('/login');
  }

  return <>
      <Navbar bg="white" data-bs-theme="light" className="shadow-lg justify-content-between">
        <Container>
          <Nav>
            <a className="navbar-brand" href="/">
              Memes app
            </a>
          </Nav>
          <Nav>
            <Button type="submit" onClick={handleLogout}>
              Logout
            </Button>
          </Nav>
        </Container>
      </Navbar>
    </>
}

export default NavbarPage;