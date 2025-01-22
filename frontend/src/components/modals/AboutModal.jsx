import React from "react";
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

const AboutModal = ({ show, onHide }) => {

  return (
    <Modal
      show={show}
      onHide={onHide}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton className="about-modal-header">
        <Modal.Title id="contained-modal-title-vcenter" >
          О проекте
        </Modal.Title>
      </Modal.Header>

      <Modal.Body className="about-modal-body">
      Мемовоз парсит весь интернет в поисках самых лучших мемов для Вас и каждый день скидывает кучу свежайших мемов из мира IT!<br/><br/>
      Также в нашем телеграм-канале <a href="https://t.me/it_memovoz">IT_мемовоз</a> Вам будет проще следить за свежим юмором!
      </Modal.Body>
      <Modal.Footer>
        <Button className="nav-button" onClick={onHide}>Закрыть</Button>
      </Modal.Footer>
    </Modal>
  );
}

export default AboutModal;
