//TODO
// обработка сообщений ошибок Login
// карточки рядом
// добавить Loading


import React, { useState, useEffect } from "react";
import FormData from 'form-data'
import ImageCard from './ImageCard.jsx'
import { useDispatch, useSelector } from "react-redux";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import { setMemes } from "../slices/memesSlice";
import { getMemes, postMeme } from "../utils/requests.js";
import NavbarPage from "./Navbar.jsx";


const IndexPage = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedName, setSelectedName] = useState(null);
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
    <div className="container h-100 p-5 my-4 overflow-hidden rounded shadow">
      <div className="row h-100 bg-white flex-md-row">
        <form onSubmit={ async (event) => {
              event.preventDefault();
              try {
                const form = new FormData();
                form.append('file', selectedImage);
                form.append('filename', selectedName);
                const postMemeResponse = await postMeme(form, access_token);
                console.log('postMemeResponse', postMemeResponse);
                const getMemesResponse = await getMemes(access_token);
                console.log('getMemesResponse', getMemesResponse)
                dispatch(setMemes(getMemesResponse.data))
              } catch (error) {
                console.log('error->', error)
              }

            }}>
        <div className="form-group">
          <label >Введите имя</label>
          <input
            className="form-control"
            type="text"
            name="name"
            onChange={(event) => {
              setSelectedName(event.target.value);
            }}
          />
          </div>
          <div className="form-group">
          <label >приложите картинку</label>
          <input
            className="form-control"
            type="file"
            name="file"
            onChange={(event) => {
              setSelectedImage(event.target.files[0]);
            }}
          />
          </div>
          <button className="btn btn-primary" type="submit">
            Загрузить файл
          </button>
        </form>
      </div>
    </div>
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