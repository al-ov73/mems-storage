import Card from 'react-bootstrap/Card';
import Image from 'react-bootstrap/Image';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import React, { useState } from "react";
import ImageModal from '../modals/ImageModal';

const ImageCard = ({ meme })  => {
  const [modalShow, setModalShow] = useState(false);

  return (
    <>
        <Image 
                height="150rem"
                src={meme.link}
                className="rounded mx-auto mt-3 d-block "
                alt='Картинка не загрузилась:('
                onClick={() => setModalShow(true)}
        />
      <ImageModal
        meme={meme}
        show={modalShow}
        onHide={() => setModalShow(false)}
      />
    </>
  );
}

export default ImageCard;
