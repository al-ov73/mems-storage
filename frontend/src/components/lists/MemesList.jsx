import React from 'react';
import ImageCard from '../cards/ImageCard.jsx'
import { useSelector } from "react-redux";
import Col from 'react-bootstrap/Col';


const MemesList = () => {
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
  
  return Object.keys(grouped).map((date, index) => {
    return <>
      <div style={{ textAlign: "center" }}>
      {index !== 0 &&  <hr style={{ width: "100%", margin: "20px auto" }} />}
        {date}
      </div>
      {grouped[date].map((meme) => {
                  return <Col className="mx-1 my-1" key={meme.id}>
                          <ImageCard meme={meme}/>
                        </Col>
                  }
          )
        }
    </>
  })

  }

export default MemesList;