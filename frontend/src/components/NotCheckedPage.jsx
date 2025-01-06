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
    return <>
      <Button variant="outline-success"
        onClick={() => navigate('/')}>
        На главную
      </Button>
      "мемов пока нет"
    </>
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
    <Row>
      <Col className="text-center my-2"><Button variant="outline-success"
        onClick={handleCheck}>
        ПРОВЕРЕНО!
      </Button></Col>
      <Col className="text-center my-2"><Button variant="outline-primary"
        onClick={() => navigate('/')}>
        На главную
      </Button></Col>
    </Row>

    {tempMemes.map((meme) => {
      return <Image
        key={meme.id}
        width="90%"
        src={meme.link}
        className="rounded mx-auto mt-3 d-block "
        alt='Картинка не загрузилась:('
        onClick={() => {
          handleDelete(meme.id)
        }} />
    })}
    <Row>
      <Col className="text-center my-2"><Button variant="outline-success"
        onClick={handleCheck}>
        ПРОВЕРЕНО!
      </Button></Col>
    </Row>

  </>
}

export default NotCheckedPage;