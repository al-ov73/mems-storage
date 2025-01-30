import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Button from 'react-bootstrap/Button';
import useAuth from '../hooks/index.js';
import { useNavigate } from "react-router-dom";
import React, { useState, } from "react";
import ChatModal from './modals/ChatModal.jsx'
import AboutModal from './modals/AboutModal';
import { getUsernameFromStorage } from '../utils/utils.js';
import { sendButtonMsgToBot } from '../utils/requests.js';


const NavbarPage = ({ full }) => {
  const auth = useAuth();
  const navigate = useNavigate();
  const [modalAboutShow, setModalAboutShow] = useState(false);
  const [modalChatShow, setModalChatShow] = useState(false);

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
    <Navbar data-bs-theme="light" className="justify-content-between">

      <Button variant="outline-primary" className='mx-4 nav-button' onClick={() => setModalChatShow(true)}>
        Чат
      </Button>

      <Button variant="outline-primary" className='mx-4 animated-button' onClick={(e) => {
        e.preventDefault();
        sendButtonMsgToBot()
        window.location.href = process.env.REACT_APP_TG_LINK;
      }}>
        В телеграмме проще <i className="fab fa-telegram-plane"></i>
      </Button>

      {full && (
        <>
          {username ? (
            <Nav>
              <Navbar.Brand>Здравствуйте, {username}</Navbar.Brand>
              <Button variant="outline-primary" className="mx-4 nav-button" type="submit" onClick={handleLogout}>
                Выйти
              </Button>
            </Nav>
          ) : (
            <Nav>
              {/* <a href="/signup">Регистрация</a> */}
                <Button variant="outline-primary" className="mx-4 nav-button" type="submit" onClick={handleLogin}>
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
    <ChatModal
        show={modalChatShow}
        onHide={() => setModalChatShow(false)}
      />
  </>
}

export default NavbarPage;