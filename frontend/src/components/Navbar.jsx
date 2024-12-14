import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import React, { useState, } from "react";
import AboutModal from './modals/AboutModal';


const NavbarPage = () => {
  const [modalAboutShow, setModalAboutShow] = useState(false);

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
      </Navbar>
      <AboutModal
        show={modalAboutShow}
        onHide={() => setModalAboutShow(false)}
      />
    </>
}

export default NavbarPage;