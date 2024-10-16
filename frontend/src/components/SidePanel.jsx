import React, { useState, useEffect } from "react";
import SpinnerEl from './spinners/SimpleSpinner';
import { Col, Row } from "react-bootstrap"
import { getTopLikedMemes } from "../utils/requests";

const TOP_LIKED_COUNT = 3;


const SidePanel = () => {
  const [isLoading, setLoading] = useState(true);
  const [topLikedMemes, setTopLikedMemes] = useState([])

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

            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default SidePanel;