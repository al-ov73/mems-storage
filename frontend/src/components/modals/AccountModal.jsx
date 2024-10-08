import React, { useState, useEffect } from "react";
import Offcanvas from 'react-bootstrap/Offcanvas';
import { getUserIdFromStorage } from '../../utils/utils';
import { getUser, signupUser } from "../../utils/requests";
import SpinnerEl from "../spinners/SimpleSpinner";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { useNavigate } from "react-router-dom";
import useAuth from "../../hooks";
import AvatarAccounCard from "../cards/AvatarAccountCard";

const AccountModal = ({ show, onHide }) => {
  const navigate = useNavigate();
  const auth = useAuth();
  const [selectedImage, setSelectedImage] = useState(null);
  const [currentUsername, setCurrentUsername] = useState('');
  const [currentFirstName, setCurrentFirstName] = useState('');
  const [currentLastName, setCurrentLastName] = useState('');
  const [currentPassword, setCurrentPassword] = useState('');
  const [
    currentPasswordConfirmation, setCurrentPasswordConfirmation
  ] = useState('');
  const [_, setCurrentPhoto] = useState('');

  const [currentUser, setCurrentUser] = useState({});
  const [isSubmitLoading, setSubmbitLoading] = useState(false);
  const [isLoading, setLoading] = useState(true);
  const access_token = localStorage.getItem('user')
  const userId = getUserIdFromStorage()
  
  // get user
  useEffect(() => {
    const inner = async () => {
      const response = await getUser(userId, access_token);
      setCurrentUser(response);
      setCurrentFirstName(currentUser.first_name)
      setCurrentLastName(currentUser.last_name)
      setCurrentPhoto(currentUser.photo)
      setLoading(false);
    }
    inner();
  }, [])
  
  const handleSubmit = (values) => async () => {
    setSubmbitLoading(true)
    try {
      const response = await signupUser(values, selectedImage)
      const { access_token } = response.data;
      if (access_token) {
        localStorage.setItem('user', access_token)
        auth.loggedIn = true;
        setSubmbitLoading(false)
        return navigate('/');
      }
    } catch (e) {
      console.log('e', e);
      setSubmbitLoading(false)
    }
  };

  if (isLoading) {
    return <SpinnerEl/>
  }
  return (
    <Offcanvas show={show} onHide={onHide}>
        <Offcanvas.Header closeButton>
          <Offcanvas.Title>{currentUser.username}</Offcanvas.Title>
        </Offcanvas.Header>
        <Offcanvas.Body>
          <AvatarAccounCard link={currentUser.photo}/>
          <Form onSubmit={handleSubmit}>
              <Form.Group className="mb-3">
              <Form.Label htmlFor="username">Ваш ник</Form.Label>
                <Form.Control type="text"
                  placeholder="Ваш ник"
                  autoComplete="username"
                  id="username"
                  onChange={(event) => {
                    setCurrentUsername(event.target.value);
                  }}
                  value={currentUsername}
                  />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label htmlFor="first_name">Ваше имя</Form.Label>
                <Form.Control type="text"
                  placeholder="Ваше имя"
                  autoComplete="first_name"
                  id="first_name"
                  onChange={(event) => {
                    setCurrentFirstName(event.target.value);
                  }}
                  value={currentFirstName}
                  />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label htmlFor="last_name">Ваша фамилия</Form.Label>
                <Form.Control type="text"
                  placeholder="Ваша фамилия"
                  autoComplete="last_name"
                  id="last_name"
                  onChange={(event) => {
                    setCurrentLastName(event.target.value);
                  }}
                  value={currentLastName}
                  />
            </Form.Group>

            <Form.Group className="mb-3" >
              <Form.Label htmlFor="password">Пароль</Form.Label>
              <Form.Control type="password"
                placeholder="Пароль"
                id="password"
                autoComplete="password"
                onChange={(event) => {
                  setCurrentPassword(event.target.value);
                }}
                value={currentPassword}
                />
            </Form.Group>

            <Form.Group className="mb-3" >
              <Form.Label htmlFor="passwordConfirmation">Подтвердите пароль</Form.Label>
              <Form.Control type="password"
                placeholder="Подтвердите пароль"
                id="passwordConfirmation"
                autoComplete="passwordConfirmation"
                onChange={(event) => {
                  setCurrentPasswordConfirmation(event.target.value);
                }}
                value={currentPasswordConfirmation}
                />
            </Form.Group>

            <Form.Label className="mt-1">Ваша фотография</Form.Label>
            <Form.Control
            className="mb-3"
              type="file"
              name="file"
              onChange={(event) => {
                setSelectedImage(event.target.files[0]);
              }}
            />
            <Button type="submit" disabled={isSubmitLoading}>
              Поменять данные
            </Button>
          </Form>
        </Offcanvas.Body>
      </Offcanvas>
  );
}

export default AccountModal;