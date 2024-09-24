import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import { useState, } from "react";

import ChatModal from './modals/ChatModal.jsx'
import useAuth from '../hooks/index.js';
import { useNavigate } from "react-router-dom";
import MemeCreateForm from "./forms/MemeCreateForm.jsx";
import { getUsernameFromStorage } from '../utils/utils.js';
import AccountModal from './modals/AccountModal.jsx';

const NavbarPage = () => {
  const auth = useAuth();
  const navigate = useNavigate();
  const [modalAccount, setModalAccount] = useState(false);
  const [modalChatShow, setModalChatShow] = useState(false);
  const [createFormShow, setCreateFormShow] = useState(false);
  const username = getUsernameFromStorage()

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
              Хранилище супер мемов
            </a>
          </Nav>
          <Button variant="outline-success"
                  onClick={() => setCreateFormShow(true)}>
                    Добавить мем
          </Button>
          
            <Button variant="outline-success" onClick={() => setModalChatShow(true)}>
              Чатик
            </Button>
            <Nav>
            <Navbar.Brand>Здравствуйте, {username}</Navbar.Brand>
            <Button className="mx-4" type="submit" onClick={handleLogout}>
              Выйти
            </Button>
            <Button className="mx-4" type="submit" onClick={() => setModalAccount(true)}>
              Аккаунт
            </Button>
          </Nav>
        </Container>
      </Navbar>

      <ChatModal
        show={modalChatShow}
        onHide={() => setModalChatShow(false)}
      />

      <MemeCreateForm
        show={createFormShow}
        onHide={() => setCreateFormShow(false)}
      />

      <AccountModal
        show={modalAccount}
        onHide={() => setModalAccount(false)}
      />
    </>
}

export default NavbarPage;