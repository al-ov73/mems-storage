import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';
import React from "react";

const NavbarPage = () => {
  return <>
      <Navbar bg="white" data-bs-theme="light" className="shadow-lg justify-content-between">
        <Container>
          <Nav>
            <a className="navbar-brand" href="/">
              Хранилище супер мемов
            </a>
          </Nav>
        </Container>
      </Navbar>
    </>
}

export default NavbarPage;