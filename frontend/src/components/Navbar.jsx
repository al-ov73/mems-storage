import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Container from 'react-bootstrap/Container';

const NavbarPage = () => {

  return <>
      <Navbar bg="white" data-bs-theme="light" className="shadow-lg justify-content-between">
        <Container>
          <Nav>
            <a className="navbar-brand" href="/">
              Memes app
            </a>
          </Nav>
        </Container>
      </Navbar>
    </>
}

export default NavbarPage;