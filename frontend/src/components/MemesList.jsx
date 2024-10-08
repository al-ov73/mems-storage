import React from 'react';
import ImageCard from './cards/ImageCard.jsx'
import { useSelector } from "react-redux";
import Col from 'react-bootstrap/Col';


const MemesList = () => {
  const currentCategory = useSelector((state) => state.categories.currentCategory);
  let memes = useSelector((state) => state.memes.memes);

  memes = (currentCategory === 'ALL') ? 
          memes :
          memes.filter((meme) => meme.category === currentCategory)

  return memes.map((meme) => {
              return <Col className="mx-1 my-1" key={meme.id}>
                      <ImageCard meme={meme}/>
                    </Col>
              }
      )
  }

export default MemesList;