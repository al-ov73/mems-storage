import { useState, useEffect } from "react";
import Offcanvas from 'react-bootstrap/Offcanvas';
import { getUserIdFromStorage } from '../../utils/utils';
import { getUser } from "../../utils/requests";
import SpinnerEl from "../spinners/SimpleSpinner";


const AccountModal = ({ show, onHide }) => {
  const [currentUser, setCurrentUser] = useState({});
  const [isLoading, setLoading] = useState(false);
  const access_token = localStorage.getItem('user')
  const userId = getUserIdFromStorage()

  // get user
  useEffect(() => {
    const inner = async () => {
      const response = await getUser(userId, access_token);
      setCurrentUser(response);
    }
    inner();
  }, [])

  if (isLoading) {
    return <SpinnerEl/>
  }
  return (
    <Offcanvas show={show} onHide={onHide}>
        <Offcanvas.Header closeButton>
          <Offcanvas.Title>{currentUser.username}</Offcanvas.Title>
        </Offcanvas.Header>
        <Offcanvas.Body>
          Some text as placeholder. In real life you can have the elements you
          have chosen. Like, text, images, lists, etc.
        </Offcanvas.Body>
      </Offcanvas>
  );
}

export default AccountModal;