import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Dropdown from 'react-bootstrap/Dropdown';
import Button from 'react-bootstrap/Button';
import useAuth from '../hooks/index.js';
import { useNavigate } from "react-router-dom";
import React, { useState, useEffect } from "react";
import ChatModal from './modals/ChatModal.jsx'
import AboutModal from './modals/AboutModal';
import { getUsernameFromStorage, getUserIdFromStorage } from '../utils/utils.js';
import { sendButtonMsgToBot, getUser } from '../utils/requests.js';
import BookmarkButton from './BookmarkButton.jsx';
import logo from '../static/memovoz-icon.ico';


const NavbarPage = ({ full }) => {
  const [userIsAdmin, setUserIsAdmin] = useState(false);
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);
  const auth = useAuth();
  const navigate = useNavigate();
  const [modalAboutShow, setModalAboutShow] = useState(false);
  const [modalChatShow, setModalChatShow] = useState(false);
  const access_token = localStorage.getItem('user')

  const username = getUsernameFromStorage()
  const userId = getUserIdFromStorage();

  useEffect(() => {
    const inner = async () => {
      if (userId) {
        const user = await getUser(userId, access_token);
        if (user.is_admin) {
          setUserIsAdmin(true)
        }
      }
    }
    inner();
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('user');
    auth.loggedIn = false;
    return navigate('/');
  }

  const handleLogin = () => {
    return navigate('/login');
  }

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 768);
    };
    window.addEventListener("resize", handleResize);
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return <>
    <Navbar data-bs-theme="light" className="justify-content-between">

      {!isMobile && (
        <>
          <Button variant="outline-primary" className='mx-4 nav-button' onClick={() => setModalChatShow(true)}>
            Чат
          </Button>
          <BookmarkButton />
          <Button variant="outline-primary" className='mx-4 animated-button' onClick={(e) => {
            e.preventDefault();
            sendButtonMsgToBot()
            window.location.href = process.env.REACT_APP_TG_LINK;
          }}>
            В телеграмме проще <i className="fab fa-telegram-plane"></i>
          </Button>
          {userIsAdmin && <Button variant="outline-primary" className='mx-4 animated-button' onClick={(e) => {
            e.preventDefault();
            sendButtonMsgToBot()
            window.location.href = `${process.env.REACT_APP_API_URL}/admin`;
          }}>
            Админ
          </Button>}
        </>
      )}

      {full && !isMobile && (
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
              <Button variant="outline-primary" className="mx-4 nav-button" type="submit" onClick={handleLogin}>
                Войти
              </Button>
            </Nav>
          )}
        </>
      )}

      {/* Кнопка dropdown для мобильного режима */}
      {isMobile && (
        <Dropdown>
          <Dropdown.Toggle variant="outline-primary" className="mx-4 nav-button" id="navbar-dropdown">
            Меню
          </Dropdown.Toggle>
          <Dropdown.Menu className="dropdown-menu">
            <Dropdown.Item onClick={() => setModalChatShow(true)}>Чат</Dropdown.Item>
            <Dropdown.Item onClick={(e) => {
              e.preventDefault();
              sendButtonMsgToBot()
              window.location.href = process.env.REACT_APP_TG_LINK;
            }}>
              В телеграмме проще <i className="fab fa-telegram-plane"></i>
            </Dropdown.Item>
            {userIsAdmin && (
              <Dropdown.Item onClick={(e) => {
                e.preventDefault();
                sendButtonMsgToBot()
                window.location.href = `${process.env.REACT_APP_API_URL}/admin`;
              }}>
                Админ
              </Dropdown.Item>
            )}
            {full && (
              <>
                {username ? (
                  <>
                    <Dropdown.Header>Здравствуйте, {username}</Dropdown.Header>
                    <Dropdown.Divider />
                    <Dropdown.Item onClick={handleLogout}>Выйти</Dropdown.Item>
                  </>
                ) : (
                  <Dropdown.Item onClick={handleLogin}>Войти</Dropdown.Item>
                )}
              </>
            )}
          </Dropdown.Menu>
        </Dropdown>
      )}
      <img
        height="50rem"
        src={logo}
        className="rounded mx-3"
        alt='Картинка не загрузилась:('
        onClick={() => navigate("/")}
      />
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