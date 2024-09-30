import Card from 'react-bootstrap/Card';
import Image from 'react-bootstrap/Image';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import React, { useState } from "react";
import ImageModal from '../modals/ImageModal';
import HeartComponent from '../Heart';
import { getUserIdFromStorage } from '../../utils/utils';

const ImageCard = ({ meme })  => {
  const [modalShow, setModalShow] = useState(false);
  const userId = getUserIdFromStorage()
  let userLike = meme.likes.find((like) => like.author_id === userId)
  const borderStyle = userId === meme.author_id ?
        'warning' :
        'secondary'

  return (
    <>
      <Card bg={borderStyle} style={{ width: '12rem' }}>
        
        <Image 
                height="150rem"
                src={meme.link}
                className="rounded mx-auto mt-3 d-block "
                alt='Картинка не загрузилась:('
                onClick={() => setModalShow(true)}
        />
        <Container>
          <Row>
            <Col align="center">{meme.name}</Col>
            {userLike && <Col xs={2}> <span className="text-danger text-end"><HeartComponent/></span></Col>}
          </Row>
        </Container>
      </Card>
      <ImageModal
        meme={meme}
        show={modalShow}
        onHide={() => setModalShow(false)}
      />
    </>
  );
}

export default ImageCard;