import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Carousel from 'react-bootstrap/Carousel';
import Image from 'react-bootstrap/Image';
import { useDispatch } from "react-redux";
import { getMemes, deleteMeme } from '../utils/requests';
import { setMemes } from "../slices/memesSlice";
import React, { useState } from "react";
import ImageModal from './ImageModal';

const ImageCard = ({ meme })  => {
  const [modalShow, setModalShow] = useState(false);
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
    <>
      <Card style={{ width: '12rem' }}>
        <Image 
                height="150rem"
                src={meme.link}
                className="rounded mx-auto mt-3 d-block "
                alt='Картинка не загрузилась:('
                onClick={() => setModalShow(true)}
        />
        <b align="center">{meme.name}</b>
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