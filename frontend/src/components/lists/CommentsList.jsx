import { Col, Row } from "react-bootstrap"


const CommentsList = ({comments}) => {
  console.log('comments', comments)

  return comments.map((comment) => {
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