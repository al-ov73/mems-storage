import { useState, useEffect } from "react";
import { Col, Row } from "react-bootstrap"
import { getComments } from "../../utils/requests";
import SpinnerEl from "../spinners/SimpleSpinner";


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
    const createdAt = comment.created_at
    const formatedDate= new Date(Date.parse(createdAt));

    const commentTime = `${formatedDate.getHours()}:${formatedDate.getMinutes()}`
    const commentDate = `${formatedDate.toLocaleDateString("ru-RU")}`
    const dateFormat = `${commentDate}: ${commentTime}`;
    
    return <Row key={comment.id} className="mb-3">
      <Col>
        <h5>{comment.author_name} </h5>
        <h6 className="fst-italic fw-light">{dateFormat} : </h6>
        <p className="overflow-hidden">{comment.text}</p>
      </Col>
    </Row>
  })
}

export default CommentsList;