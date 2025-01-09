import React from "react";
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import { Row } from "react-bootstrap";

const WelcomeModal
  = ({ show, onHide }) => {

    return (
      <Modal
        show={show}
        onHide={onHide}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
      >
        <Modal.Header>
          <Modal.Title id="contained-modal-title-vcenter">
          <p className="text-center">Где это ты?</p>
          </Modal.Title>
        </Modal.Header>

        <Modal.Body>
          <p className="fs-4">Мемовоз парсит весь интернет в поисках самых лучших мемов для Вас и <span className="fw-bold">каждый день</span> скидывает кучу свежайших мемов из мира IT!</p>
          <br />
          <p className="fs-4 fst-italic">Также в нашем телеграм-канале <a href={process.env.REACT_APP_TG_LINK}>IT_мемовоз</a> Вам будет проще следить за свежим юмором!</p>
          <Row><Button variant="success" size="lg" onClick={onHide}>ПОЕХАЛИ !</Button></Row>
        </Modal.Body>
      </Modal>
    );
  }

export default WelcomeModal
  ;
