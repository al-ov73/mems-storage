import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { useDispatch } from "react-redux";
import { FormikProvider, useFormik } from "formik";
import Form from 'react-bootstrap/Form';
import { useState } from "react";

const ws = new WebSocket(`ws://127.0.0.1:8000/chat/ws`);


const ChatModal = ({ show, onHide }) => {
  const [messages, setMessages] = useState([]);

  console.log('messages', typeof messages)
  // ws.addEventListener('open', (event) => {console.log('WebSocket connection opened');});
  // ws.addEventListener('message', (event) => {console.log('Received message:', event.data);});
  // ws.addEventListener('error', (event) => {console.error('WebSocket error:', event);});
  // ws.addEventListener('close', (event) => {console.log('WebSocket connection closed:', event.code, event.reason);});

  ws.onmessage = (event) => {
    const newMessage = event.data
    console.log('receieved message', typeof newMessage);
    console.log('messages old', typeof messages)
    const newListOfMessages = messages.push(newMessage);
    console.log('newListOfMessages', typeof newListOfMessages)
    setMessages(newListOfMessages)
  };

  const handleMessageSubmit = async (event) => {
    try {
      console.log('message send from frontend->', event)
      ws.send(event.message)
    } catch (e) {
      console.log(e);
    }
  }

    const formik = useFormik({
        initialValues: {
            message: '',
        },
        onSubmit: (messageObject, { resetForm }) => {
        handleMessageSubmit(messageObject);
        resetForm();
        },
    });

  return (
    <Modal
      show={show}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          Чатик
        </Modal.Title>
      </Modal.Header>

      <Modal.Body>
      <FormikProvider value={formik}>
                    <Form onSubmit={formik.handleSubmit} noValidate="" className="py-1 border-0"> 
                      <Form.Group className="input-group has-validation">
                      <Form.Control
                        aria-label="Введите сообщение"
                        placeholder=""
                        autoComplete="message"
                        id="message"
                        name="message"
                        type="text"
                        className=" border border-dark border-2 rounded-4 p-0 ps-2"
                        onChange={formik.handleChange}
                        value={formik.values.message} />
                        
                        <button type="submit" disabled="" className="btn btn-group-vertical">
                          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="20" height="20" fill="currentColor">
                            <path fillRule="evenodd" d="M15 2a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1zM0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2zm4.5 5.5a.5.5 0 0 0 0 1h5.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L10.293 7.5z"></path>
                          </svg>
                          <span className="visually-hidden">Отправить</span>
                        </button>

                      </Form.Group>
                    </Form>
                  </FormikProvider>
      </Modal.Body>

      <Modal.Footer>
        <Button onClick={onHide}>Закрыть</Button>
      </Modal.Footer>
    </Modal>
  );
}

export default ChatModal;