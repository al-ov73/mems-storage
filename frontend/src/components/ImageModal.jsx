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
import { getMemes, deleteMeme, postLabel } from '../utils/requests';
import { setMemes } from "../slices/memesSlice";

const ImageModal = ({ meme, show, onHide }) => {
  const [selectedLabel, setSelectedLabel] = useState(null);
  const access_token = localStorage.getItem('user')
  const dispatch = useDispatch();

  const handleDelete = async (id, token) => {
    const deleteResponse = await deleteMeme(id, token)
    console.log('deleteResponse', deleteResponse);
    const getMemesResponse = await getMemes(token);
    console.log('getMemesResponse', getMemesResponse)
    dispatch(setMemes(getMemesResponse.data))    
  }

  return (
    <Modal
      show={show}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          Название мема: {meme.name}
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
      <Container>
        <Row xs="auto" className="my-3">
          {meme.meme_labels && meme.meme_labels.map((label) => {
                    return <>
                      <Col key={label.id}>{label.title}</Col>
                    </>
                  })}
                  <Col>
        <Form onSubmit={ async (event) => {
                  event.preventDefault();
                  try {
                    const form = new FormData();
                    form.append('title', selectedLabel);
                    form.append('meme_id', meme.id);
                    const postLabelResponse = await postLabel(form, access_token);
                    console.log('postLabelResponse', postLabelResponse)
                  } catch (error) {
                    console.log('error->', error)
                  }
                }}>
              <Form.Group>
                <Form.Control
                  placeholder="Введите тег"
                  type="text"
                  name="label"
                  onChange={(event) => {
                    setSelectedLabel(event.target.value);
                  }}
                />
              
                
              </Form.Group>
            </Form>        
            </Col>  
        </Row>
        <Row xs="auto">
        <Button variant="primary"
                onClick={() => handleDelete(meme.id, access_token)}>
            Удалить
        </Button>
        <Button onClick={onHide}>Закрыть</Button>          
        </Row>
        </Container>
      </Modal.Footer>
    </Modal>
  );
}

export default ImageModal;