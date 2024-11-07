import React, { useState, useEffect } from "react";
import SpinnerEl from './spinners/SimpleSpinner';
import { Col, Form, Row } from "react-bootstrap"
import { getTopLikedMemes, postQuestion } from "../utils/requests";

const TOP_LIKED_COUNT = 3;


const SidePanel = () => {
  const [isLoading, setLoading] = useState(true);
  const [isQuestionLoading, setQuestionLoading] = useState(false);
  const [topLikedMemes, setTopLikedMemes] = useState([])
  const [question, setQuestion] = useState('');
  const [gigaResponse, setGigaResponse] = useState('');
  const access_token = localStorage.getItem('user')

  // get top liked memes
  useEffect(() => {
    const inner = async () => {
      const response = await getTopLikedMemes(access_token, TOP_LIKED_COUNT);
      setTopLikedMemes(response);
      setLoading(false);
    }
    inner();
  }, [])

  if (isLoading) {
    return <SpinnerEl/>
  }

  return (
    <>
      <div className="sidebar" role="cdb-sidebar">
        <div className="sidebar-container">
          <div className="sidebar-nav">
            <div className="sidenav">
              <h6>Топ лучших мемов</h6>
              {topLikedMemes.map((meme) => {
                return <Row key={meme.id}>
                  <Col>
                    <a href="">{meme.name}</a>: {meme.likes_count} лайков
                  </Col>
                </Row>
              })}
              <h6>Задай любой вопрос:</h6>
              <Row className="my-3">
                <Col>
                  <Form onSubmit={async (event) => {
                    event.preventDefault();
                    try {
                      const form = new FormData();
                      form.append('question', question);
                      setQuestionLoading(true);
                      const response = await postQuestion(form, access_token);
                      setQuestionLoading(false);
                      setGigaResponse(response.data)
                      setQuestion('');
                    } catch (error) {
                      console.log('error->', error)
                    }
                  }}>
                    <Form.Group>
                      <Form.Control
                        placeholder="Напишите вопрос ..."
                        type="text"
                        name="question"
                        onChange={(event) => {
                          setQuestion(event.target.value);
                        }}
                        value={question}
                      />
                    </Form.Group>
                  </Form>
                </Col>
              </Row>
              <Row>
                {isQuestionLoading ? <SpinnerEl /> : gigaResponse}
              </Row>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default SidePanel;