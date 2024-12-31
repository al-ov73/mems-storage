import { Carousel, Row, Modal, Image, Button, Col, Container } from 'react-bootstrap';
import React, { useState, useEffect } from "react";
import { deleteMeme, getNotCheckedMemes, sendCheckedMemes } from '../utils/requests.js';
import { useNavigate } from "react-router-dom";


const NotCheckedPage = () => {
  const navigate = useNavigate();
  const [tempMemes, setTempMemes] = useState([]);
  const access_token = localStorage.getItem('user')
  
  // get memes
  useEffect(() => {
    const inner = async () => {
      try {
        const response = await getNotCheckedMemes(access_token)
        setTempMemes(response.data)
      } catch (e) {
        console.log('memes get error');
        console.log(e)
        setTempMemes([])
      }      
    }
    inner();
  }, []);

  if (tempMemes.length === 0) {
        return "мемов пока нет"
  }

  
  const handleDelete = async (id, token) => {
    await deleteMeme(id, token)
    const response = await getNotCheckedMemes(access_token)
    setTempMemes(response.data)  
  }
  
  const handleCheck = async () => {
    const ids = tempMemes.map((meme) => meme.id)
    await sendCheckedMemes(access_token, ids)
    window.location.reload();
  }

  return <>
    <Button variant="outline-success"
            onClick={handleCheck}>
        ПРОВЕРЕНО!
    </Button>
    <Button variant="outline-success"
            onClick={() => navigate('/')}>
        На главную
    </Button>
  <Row>
    {
      tempMemes.map((meme) => {
        return <Col className="mx-1 my-1" key={meme.id}>
                    <Image 
                          height="150rem"
                          src={meme.link}
                          className="rounded mx-auto mt-3 d-block "
                          alt='Картинка не загрузилась:('
                          onClick={() => {
                            handleDelete(meme.id)
                          }}
                  />
                </Col>
          })}
  </Row></>
  }

export default NotCheckedPage;