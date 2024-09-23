import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Carousel from 'react-bootstrap/Carousel';
import Image from 'react-bootstrap/Image';
import { useDispatch } from "react-redux";
import { getMemes, deleteMeme } from '../utils/requests';
import { setMemes } from "../slices/memesSlice";
import React, { useState } from "react";
import ImageModal from './ImageModal';
import HeartComponent from './Heart';

const ImageCard = ({ meme })  => {
  const [modalShow, setModalShow] = useState(false);

  return (
    <>
      <Card style={{ width: '12rem' }}>
        
        <Image 
                height="150rem"
                src={meme.link}
                className="rounded mx-auto mt-3 d-block "
                alt='Картинка не загрузилась:('
                onClick={() => setModalShow(true)}
        /><span class="text-danger text-end"><HeartComponent/></span>
        <span align="center">
          {meme.name}
        </span>
        
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