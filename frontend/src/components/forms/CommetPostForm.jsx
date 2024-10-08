import React, { useState } from "react";
import FormData from 'form-data'
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { useDispatch } from "react-redux";

import { getMemes, postComment } from '../../utils/requests';
import { setMemes } from "../../slices/memesSlice";


const CommentPostForm = ({ memeId }) => {
  const [comment, setComment] = useState('');
  const access_token = localStorage.getItem('user')
  const dispatch = useDispatch();

  return <>
  <Row className="my-3">
    <Col>
      <Form onSubmit={ async (event) => {
                event.preventDefault();
                try {
                  const form = new FormData();
                  form.append('text', comment);
                  form.append('meme_id', memeId);
                  setComment('')
                  await postComment(form, access_token);
                  const getMemesResponse = await getMemes(access_token);
                  dispatch(setMemes(getMemesResponse.data))
                } catch (error) {
                  console.log('error->', error)
                }
              }}>
        <Form.Group>
          <Form.Control
            placeholder="Напишите комментарий ..."
            type="text"
            name="comment"
            onChange={(event) => {
              setComment(event.target.value);
            }}
            value={comment}
          />
        </Form.Group>
      </Form>        
    </Col>  
  </Row>
  </>
}

export default CommentPostForm