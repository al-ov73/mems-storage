import React, { useState, useEffect } from "react";
import { Col, Row } from "react-bootstrap"
import { convertDateTime } from "../../utils/utils";


const CommentsList = ({ memeComments }) => {
  if (!memeComments) {
    return "комментариев пока нет"
  }
  
  return memeComments.map((comment) => {
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