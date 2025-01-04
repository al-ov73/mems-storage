import React, { useEffect } from "react";
import { useDispatch } from "react-redux";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import { setMemes } from "../slices/memesSlice";
import { getMemes } from "../utils/requests.js";
import NavbarPage from "./Navbar.jsx";
import MemesList from "./lists/MemesList.jsx";


const IndexPage = () => {
  const dispatch = useDispatch();

  // get memes
  useEffect(() => {
    const inner = async () => {
      try {
        const response = await getMemes(access_token)
        dispatch(setMemes(response.data))
      } catch (e) {
        console.log('memes get error');
        console.log(e)
        dispatch(setMemes([]))
      }      
    }
    inner();
  }, []);

  const access_token = localStorage.getItem('user')

  return (
    <>
    <NavbarPage full={true}/>
    <Container className="d-flex">
      <Container>
        <Row>
          <MemesList/>
        </Row>
      </Container>
    </Container>
  </>
  );
}

export default IndexPage;