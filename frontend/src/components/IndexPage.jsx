import React, { useState, useEffect } from "react";
import FormData from 'form-data'
import ImageCard from './ImageCard.jsx'
import { useDispatch, useSelector } from "react-redux";
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';

import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import { setMemes } from "../slices/memesSlice";
import { getMemes, postMeme, getCategories } from "../utils/requests.js";
import NavbarPage from "./Navbar.jsx";
import config from "../config/config.js";
import MemeCreateForm from "./MemeCreateForm.jsx";


const IndexPage = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedName, setSelectedName] = useState(null);
  const [categories, setCategories] = useState([]);
  const [createFormShow, setCreateFormShow] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const dispatch = useDispatch();

  const memes = useSelector((state) => state.memes.memes);
  const access_token = localStorage.getItem('user')

  useEffect(() => {
    const inner = async () => {
      try {
        const response = await getMemes(access_token)
        console.log('getMemes response', response)
        dispatch(setMemes(response.data))
      } catch (e) {
        console.log('memes get error');
        console.log(e)
      }      
    }
    inner();
  }, []);
  
  return (
    <>
    <NavbarPage/>
    <Button variant="outline-success" onClick={() => setCreateFormShow(true)}>Добавить мем</Button>
    <MemeCreateForm
        show={createFormShow}
        onHide={() => setCreateFormShow(false)}
      />
    <Container>
      <Row>
        {memes && <>
            {memes.map((meme) => {
              return <Col xs={6} md={4} className="mx-4 my-1" key={meme.id}>
                      <ImageCard meme={meme}/>
                    </Col>
              }
            )}
        </>}
        </Row>
    </Container>
  </>
  );
}

export default IndexPage;