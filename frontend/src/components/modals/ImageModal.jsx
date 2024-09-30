import { useState } from "react";
import FormData from 'form-data'
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Image from 'react-bootstrap/Image';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { useDispatch } from "react-redux";
import { getMemes, deleteMeme, postLabel } from '../../utils/requests';
import { setMemes } from "../../slices/memesSlice";
import CommentPostForm from "../forms/CommetPostForm";
import CommentsList from "../lists/CommentsList";
import LikeButton from "../LikeButton";
import LabelPostForm from "../forms/LabelPostForm";
import { convertDateTime, getUserIdFromStorage } from "../../utils/utils";

const ImageModal = ({ meme, show, onHide }) => {
  const access_token = localStorage.getItem('user')
  const dispatch = useDispatch();
  const userId = getUserIdFromStorage();

  const handleDelete = async (id, token) => {
    const deleteResponse = await deleteMeme(id, token)
    console.log('deleteResponse', deleteResponse);
    const getMemesResponse = await getMemes(token);
    console.log('getMemesResponse', getMemesResponse)
    dispatch(setMemes(getMemesResponse.data))    
  }

  const dateFormat = convertDateTime(meme.created_at)

  return (
    <Modal
      show={show}
      onHide={onHide}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          {meme.name}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
      <Image 
                height="330rem"
                src={meme.link}
                className="rounded mx-auto d-block"
                alt='Картинка не загрузилась:('/>
      </Modal.Body>
      <Modal.Footer>
      <footer className="blockquote-footer">
           Загрузил {meme.author.username} {dateFormat}
          </footer>
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