import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import useAuth from '../hooks/index.js';
import { useNavigate } from "react-router-dom";
import React, { useState, } from "react";
import AboutModal from './modals/AboutModal';
import { getUsernameFromStorage } from '../utils/utils.js';


const NavbarPage = ({full}) => {
  const auth = useAuth();
  const navigate = useNavigate();
  const [modalAboutShow, setModalAboutShow] = useState(false);
  const username = getUsernameFromStorage()

  const handleLogout = () => {
    localStorage.removeItem('user');
    auth.loggedIn = false;
    return navigate('/');
  }

  const handleLogin = () => {
    return navigate('/login');
  }

  return <>
      <Navbar bg="white" data-bs-theme="light" className="shadow-lg justify-content-between">
        <Container>
          <Button variant="outline-success" onClick={() => setModalAboutShow(true)}>
              О проекте
            </Button>
          <Nav>
            <a className="navbar-brand" href="/">
              Мемовоз всегда привозит свежие мемы
            </a>
          </Nav>
        </Container>
        {full && (
          <>
            {username ? (
              <Nav>
                <Navbar.Brand>Здравствуйте, {username}</Navbar.Brand>
                <Button className="mx-4" type="submit" onClick={handleLogout}>
                  Выйти
                </Button>
              </Nav>
            ) : (
              <Nav>
                {/* <a href="/signup">Регистрация</a> */}
                <Button className="mx-4" type="submit" onClick={handleLogin}>
                  Войти
                </Button>
              </Nav>
            )}
          </>
        )}
      </Navbar>
      <AboutModal
        show={modalAboutShow}
        onHide={() => setModalAboutShow(false)}
      />
    </>
}

export default NavbarPage;