import { useSelector } from "react-redux";
import { useDispatch } from "react-redux";

import { Image, Col } from 'react-bootstrap';
import React, { useState, } from "react";
import { setMemes } from "../../slices/memesSlice";
import { deleteMeme, getMemes } from '../../utils/requests';
import ImageModal from "../modals/ImageModal.jsx";


const MemesList = ({ memeOffset, memesPerPage }) => {
  const [modalShow, setModalShow] = useState(false);
  const [currentMeme, setCurrentMeme] = useState({});
  const [currentIndex, setCurrentIndex] = useState(0);

  const dispatch = useDispatch();
  const access_token = localStorage.getItem('user')

  let memes = useSelector((state) => state.memes.memes);

  if (memes.length === 0) {
    return <p>мемов пока нет</p>
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

  const handleDelete = async (id, token) => {
    await deleteMeme(id, token)
    const getMemesResponse = await getMemes(access_token, memeOffset, memesPerPage);
    dispatch(setMemes(getMemesResponse.data))
    setCurrentMeme(memes[currentIndex + 1])
    setCurrentIndex(currentIndex + 1);
  }

  return Object.keys(grouped).map((date, index) => {
    return <React.Fragment key={index}>
      {/* DATE WITH <hr> */}
      <div style={{ textAlign: "center" }}>
        {index !== 0 && <hr style={{ width: "100%", margin: "20px auto" }} />}
        {date}
      </div>
      {/* END DATE WITH <hr> */}

      {/* IMAGE CARD */}
      {grouped[date].map((meme) => {
        return <Col className="mx-1 my-1" key={meme.id}>
          <Image
            height="150rem"
            src={meme.preview || meme.link}
            className="hover-target rounded mx-auto mt-3 d-block img-card"
            alt='Картинка не загрузилась:('
            onClick={() => {
              setCurrentMeme(meme)
              setCurrentIndex(memes.indexOf(meme))
              setModalShow(true)
            }}
          />
        </Col>
      })}
      {/* END IMAGE CARD */}

      {modalShow && (
        <ImageModal
          memeId={currentMeme.id}
          memeOffset={memeOffset}
          memesPerPage={memesPerPage}
          show={modalShow}
          onHide={() => setModalShow(false)}
        />
      )}
    </React.Fragment>
  })

}

export default MemesList;