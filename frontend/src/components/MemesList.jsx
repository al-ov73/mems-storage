import React from 'react';
import ImageCard from './cards/ImageCard.jsx'
import { useSelector } from "react-redux";
import Col from 'react-bootstrap/Col';


const MemesList = () => {
  let memes = useSelector((state) => state.memes.memes);
  if (memes.length === 0) {
        return "мемов пока нет"
  }
  return memes.map((meme) => {
              return <Col className="mx-1 my-1" key={meme.id}>
                      <ImageCard meme={meme}/>
                    </Col>
              }
      )
  }

export default MemesList;