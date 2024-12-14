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
              <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          О проекте
        </Modal.Title>
      </Modal.Header>

      <Modal.Body>
      Мемовоз парсит весь интернет в поисках самых лучших мемов для Вас и каждый день скидывает кучу свежайших мемов из мира IT!
      </Modal.Body>
      <Modal.Footer>
        <Button onClick={onHide}>Закрыть</Button>
      </Modal.Footer>
    </Modal>
  );
}

export default AboutModal;
