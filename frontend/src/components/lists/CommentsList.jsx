import React, { useState, useEffect } from "react";
import { Col, Row } from "react-bootstrap"
import { getComments } from "../../utils/requests";
import SpinnerEl from "../spinners/SimpleSpinner";
import { convertDateTime } from "../../utils/utils";


const CommentsList = ({ memeId }) => {
  const [loading, setLoading] = useState(true);
  const [memeComments, setMemeComments] = useState([]);
  const access_token = localStorage.getItem('user')

  useEffect(() => {
    const inner = async () => {
      const comments = await getComments(memeId, access_token)
      setMemeComments(comments)
      setLoading(false)
    }
    inner();
  }, [])

  return loading ? <SpinnerEl /> 
    : memeComments.map((comment) => {
    const dateFormat = convertDateTime(comment.created_at)
    
    return <Row key={comment.id} className="mb-3">
      <Col>
        <h5>{comment.author_name} <small className="fs-6 fst-italic fw-light">{dateFormat}</small></h5>
        <p className="overflow-hidden">{comment.text}</p>
      </Col>
    </Row>
  })
}

export default CommentsList;