import { useSelector } from "react-redux";
import { useDispatch } from "react-redux";
import { Carousel, Row, Modal, Image, Button, Col, Container } from 'react-bootstrap';
import React, { useState, useEffect } from "react";
import CommentPostForm from "../forms/CommetPostForm";
import CommentsList from "../lists/CommentsList";
import LikeButton from "../LikeButton";
import { setMemes } from "../../slices/memesSlice";
import LabelPostForm from "../forms/LabelPostForm";
import { getUsernameFromStorage, getUserIdFromStorage } from '../../utils/utils.js';
import { getUser, deleteMeme, getMemes } from '../../utils/requests';


const MemesList = () => {
  const [userIsAdmin, setUserIsAdmin] = useState(false);
  const [modalShow, setModalShow] = useState(false);
  const [currentMeme, setCurrentMeme] = useState({});
  const [currentIndex, setCurrentIndex] = useState(0);
  const username = getUsernameFromStorage()
  const dispatch = useDispatch();
  const access_token = localStorage.getItem('user')
  const userId = getUserIdFromStorage();
  
  useEffect(() => {
    const inner = async () => {
      if (userId) {
        const user = await getUser(userId, access_token);
        if (user.is_admin) {
          setUserIsAdmin(true)
      }
      }
    }
    inner();
  }, [])

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

  const handleDelete = async (id, token) => {
    await deleteMeme(id, token)
    const getMemesResponse = await getMemes(token);
    dispatch(setMemes(getMemesResponse.data))    
  }

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

      {/* MODAL */}

      {setModalShow && (
            <Modal
            show={modalShow}
            onHide={() => setModalShow(false)}
            size="lg"
            centered
            >
              <Modal.Body style={{ display: 'flex', height: '500px', alignItems: 'center', justifyContent: 'center' }}>
                  <Carousel activeIndex={currentIndex} onSelect={handleSelect} variant='dark' interval={null} indicators={false}>
                    {memes.map(meme => (
                      <Carousel.Item
                      key={meme.id}>
                          <img
                            height="100%"
                            style={{
                              maxHeight: `500px`,
                              width: 'auto',
                            }}
                            src={meme.link}
                            className="img-fluid rounded p-3"
                            alt='Картинка не загрузилась:('
                          />
                        </Carousel.Item>
                      ))}
                  </Carousel>
                </Modal.Body>
              <Modal.Footer>
                <Container>
                <Row className="my-3">
                  <Col className="my-1" sm={6}><LikeButton meme={currentMeme}/></Col>
                  <Col className="my-1">
                    {
                      userIsAdmin &&
                        <Button variant="outline-danger"
                                onClick={() => handleDelete(currentMeme.id, access_token)}>
                            Удалить
                        </Button>            
                    }

                  </Col>
                  <Col className="my-1">
                  <Button onClick={() => setModalShow(false)}>Закрыть</Button> 
                  </Col>
                  </Row>

                  {/* LABELS */}
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
                    {/* LABEL POST FORM */}
                      {username && (
                      <Col className="my-1">
                        <LabelPostForm meme={currentMeme}/>
                      </Col>  
                      )}
                  </Row>

                  {/* COMMENTS */}
                  {username && <CommentPostForm memeId={currentMeme.id}/>}
                  {!username && 'Зарегистрируйтесь, чтобы оставлять комментерии и ставить лайки'}
                  
                  <CommentsList memeId={currentMeme.id}/>
                  </Container>
                </Modal.Footer>
              </Modal>
              // END MODAL
      )}
    </>
  })

  }

export default MemesList;