import React from "react";
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Image from 'react-bootstrap/Image';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { useSelector } from "react-redux";
import Carousel from 'react-bootstrap/Carousel';
import { useDispatch } from "react-redux";
import { getMemes, deleteMeme, getUser } from '../../utils/requests';
import { setMemes } from "../../slices/memesSlice";
import CommentPostForm from "../forms/CommetPostForm";
import CommentsList from "../lists/CommentsList";
import LikeButton from "../LikeButton";
import LabelPostForm from "../forms/LabelPostForm";
import { convertDateTime, getUserIdFromStorage } from "../../utils/utils";

const ImageModal = ({ meme, index, show, onHide }) => {
  const access_token = localStorage.getItem('user')
  const dispatch = useDispatch();
  const userId = getUserIdFromStorage();

  let memes = useSelector((state) => state.memes.memes);

  const handleDelete = async (id, token) => {
    const deleteResponse = await deleteMeme(id, token)
    const getMemesResponse = await getMemes(token);
    dispatch(setMemes(getMemesResponse.data))    
  }

  // const dateFormat = convertDateTime(meme.created_at)

  return (
    <Modal
      show={show}
      onHide={onHide}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
            <Carousel controls indicators activeIndex={index}>
              {memes.map(meme => (
                  <Carousel.Item key={meme.id}>
                    <img
                      className="testimonialImages d-block w-50"
                      src={meme.link}
                    />
                  </Carousel.Item>
                ))}

        </Carousel>


      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          {meme.name}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
      <Image 
                width="100%"
                src={meme.link}
                className="rounded mx-auto d-block"
                alt='Картинка не загрузилась:('/>
      </Modal.Body>
      <Modal.Footer>
      <Container>
      <Row className="my-3">
        <Col className="my-1" sm={6}><LikeButton meme={meme}/></Col>
        <Col className="my-1">
          {
            userId === meme.author_id &&
              <Button variant="outline-danger"
                      onClick={() => handleDelete(meme.id, access_token)}>
                  Удалить
              </Button>            
          }

        </Col>
        <Col className="my-1">
        <Button onClick={onHide}>Закрыть</Button> 
        </Col>
        </Row>
        <Row xs="auto" className="my-3">
          {meme.meme_labels && meme.meme_labels.map((label) => {
                    return <Col key={label.id} className="my-1">
                              <Button className="rounded-pill"
                                      variant="warning"
                                      size="sm"
                                      onClick={onHide}>{label.title}
                              </Button>  
                            </Col>
                  })}
            <Col className="my-1">
              <LabelPostForm meme={meme}/>
            </Col>  
        </Row>
        <CommentPostForm memeId={meme.id}/>
        <CommentsList memeId={meme.id}/>
        </Container>
      </Modal.Footer>
    </Modal>
  );
}

export default ImageModal;
