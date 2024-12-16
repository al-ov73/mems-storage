
import ImageCard from '../cards/ImageCard.jsx'
import { useSelector } from "react-redux";
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Image from 'react-bootstrap/Image';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import React, { useState } from "react";
import ImageModal from '../modals/ImageModal';
import Carousel from 'react-bootstrap/Carousel';
import CommentPostForm from "../forms/CommetPostForm";
import CommentsList from "../lists/CommentsList";
import LikeButton from "../LikeButton";
import LabelPostForm from "../forms/LabelPostForm";
import { getUsernameFromStorage } from '../../utils/utils.js';


const MemesList = () => {
  const [modalShow, setModalShow] = useState(false);
  const [currentMeme, setCurrentMeme] = useState({});
  const [currentIndex, setCurrentIndex] = useState(0);
  const username = getUsernameFromStorage()
  let memes = useSelector((state) => state.memes.memes);
  if (memes.length === 0) {
        return "мемов пока нет"
  }

  const grouped = {};
  memes.forEach(meme => {
    const parts = meme.created_at.split('T');
    const createdDate = parts[0];
    if (!grouped[createdDate]) {
      grouped[createdDate] = [];
    }
    grouped[createdDate].push(meme);
  })
  const handleSelect = (selectedIndex) => {
    setCurrentIndex(selectedIndex);
  };

  return Object.keys(grouped).map((date, index) => {
    return <>
      <div style={{ textAlign: "center" }}>
      {index !== 0 &&  <hr style={{ width: "100%", margin: "20px auto" }} />}
        {date}
      </div>
      {grouped[date].map((meme) => {
                  return <Col className="mx-1 my-1" key={meme.id}>
                            <Image 
                                  height="150rem"
                                  src={meme.link}
                                  className="rounded mx-auto mt-3 d-block "
                                  alt='Картинка не загрузилась:('
                                  onClick={() => {
                                    setCurrentMeme(meme)
                                    setCurrentIndex(memes.indexOf(meme))
                                    setModalShow(true)
                                  }}
                          />
                        </Col>
                  }
          )
        }
      {setModalShow && (
            <Modal
            show={modalShow}
            onHide={() => setModalShow(false)}
            size="lg"
            aria-labelledby="contained-modal-title-vcenter"
            centered
          >
                  <Carousel activeIndex={currentIndex} onSelect={handleSelect} variant='dark' interval={null}>
                    {memes.map(meme => (
                        <Carousel.Item key={meme.id}>
                          <img
                            height="80%"
                            src={meme.link}
                            className="rounded mx-auto d-block"
                            alt='Картинка не загрузилась:('
                          />
                        </Carousel.Item>
                      ))}
      
              </Carousel>
              <Modal.Footer>
                <Container>
                <Row className="my-3">
                  <Col className="my-1" sm={6}><LikeButton meme={currentMeme}/></Col>
                  <Col className="my-1">

                  </Col>
                  <Col className="my-1">
                  <Button onClick={() => setModalShow(false)}>Закрыть</Button> 
                  </Col>
                  </Row>
                  <Row xs="auto" className="my-3">
                    {currentMeme.meme_labels && currentMeme.meme_labels.map((label) => {
                              return <Col key={label.id} className="my-1">
                                        <Button className="rounded-pill"
                                                disabled={!Boolean(username)}
                                                variant="warning"
                                                size="sm"
                                                onClick={() => setModalShow(false)}>
                                                {label.title}
                                        </Button>  
                                      </Col>
                            })}
                      {username && (
                      <Col className="my-1">
                        <LabelPostForm meme={currentMeme}/>
                      </Col>  
                      )}
                  </Row>
                  {username && <CommentPostForm memeId={currentMeme.id}/>}
                  <CommentsList memeId={currentMeme.id}/>
                  </Container>
                </Modal.Footer>
              </Modal>
      )}
    </>
  })

  }

export default MemesList;