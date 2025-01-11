import React, { useState, useEffect } from "react";
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { useSelector } from "react-redux";
import { useDispatch } from "react-redux";
import { getMemes, deleteMeme, getUser } from '../../utils/requests';
import { setMemes } from "../../slices/memesSlice";
import CommentPostForm from "../forms/CommetPostForm";
import CommentsList from "../lists/CommentsList";
import LikeButton from "../LikeButton";
import LabelPostForm from "../forms/LabelPostForm";
import { getUserIdFromStorage, getUsernameFromStorage } from "../../utils/utils";
import LabelsList from "../lists/LabelsList";

const ImageModal = ({ memeId, memeOffset, memesPerPage, show, onHide }) => {
  const [userIsAdmin, setUserIsAdmin] = useState(false);
  const access_token = localStorage.getItem('user')
  const dispatch = useDispatch();

  const userId = getUserIdFromStorage();
  const username = getUsernameFromStorage();
  const memes = useSelector((state) => state.memes.memes);
  const currentMeme = memes.find((meme) => meme.id === memeId)

  useEffect(() => {
    const inner = async () => {
      if (userId) {
        const user = await getUser(userId, access_token);
        if (user.is_admin) {
          setUserIsAdmin(true)
        }
      }
    }
    inner();
  }, [])

  const handleDelete = async (id, token) => {
    await deleteMeme(id, token)
    const getMemesResponse = await getMemes(access_token, memeOffset, memesPerPage);
    dispatch(setMemes(getMemesResponse.data))
    onHide()
  }

  // const dateFormat = convertDateTime(meme.created_at)

  return (
    <Modal
      show={show}
      onHide={onHide}
      size="lg"
      centered
    >
      <Modal.Body style={{ display: 'flex', height: '500px', alignItems: 'center', justifyContent: 'center' }}>
        <img
          height="100%"
          style={{
            maxHeight: `500px`,
            width: 'auto',
          }}
          src={currentMeme.link}
          className="img-fluid rounded p-3"
          alt='Картинка не загрузилась:('
        />
      </Modal.Body>
      <Modal.Footer>
        <Container>

          <Row className="my-3">

            <Col className="my-1" sm={6}>
              <LikeButton meme={currentMeme} memeOffset={memeOffset} memesPerPage={memesPerPage} />
            </Col>

            <Col className="my-1">
              {userIsAdmin && <Button variant="outline-danger"
                onClick={() => handleDelete(currentMeme.id, access_token)}>
                Удалить
              </Button>}

            </Col>
            <Col className="my-1">
              <Button onClick={onHide}>Закрыть</Button>
            </Col>
          </Row>

          <LabelsList currentMeme={currentMeme} username={username} memeOffset={memeOffset} memesPerPage={memesPerPage} />

          {/* COMMENTS */}
          {username && <CommentPostForm memeId={currentMeme.id} memeOffset={memeOffset} memesPerPage={memesPerPage} />}
          {!username && 'Зарегистрируйтесь, чтобы оставлять комментерии и ставить лайки'}
          <CommentsList memeComments={currentMeme.comments} />
          
        </Container>
      </Modal.Footer>
    </Modal>
  );
}

export default ImageModal;
