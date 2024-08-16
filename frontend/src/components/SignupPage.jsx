import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { useDispatch } from 'react-redux'
import { useNavigate } from "react-router-dom";
import { FormikProvider, useFormik, ErrorMessage } from "formik";
import * as Yup from 'yup';
import axios from 'axios';

import routes from '../utils/routes.js';
import useAuth from '../hooks/index.js';
import IndexNavbar from './Navbar.jsx';
import { signupUser } from '../utils/requests.js';

const SignupPage = () => {
  const dispatch = useDispatch()
  const navigate = useNavigate();
  const auth = useAuth();
  const [isLoading, setLoading] = useState(false);

  const SignupSchema = Yup.object().shape({
    username: Yup.string()
      .min(3, 'от 3 о 20 символов')
      .max(20, 'от 3 о 20 символов')
      .required('required field'),
    password: Yup.string().min(2, 'больше 2 символов'),
    passwordConfirmation: Yup.string()
      .oneOf([Yup.ref('password'), null], 'Пароли должны совпадать'),
  });


  const handleSubmit = (values, actions) => async () => {
    setLoading(true)
    try {
      const response = await signupUser(values)
      console.log('response', response.data)
      auth.loggedIn = true;
      setLoading(false)
      return navigate('/');
    } catch (e) {
      console.log('e', e);
      setLoading(false)
    }
  };

  const formik = useFormik({
    initialValues: {
      username: '',
      password: '',
      passwordConfirmation: '',
    },
    validationSchema: SignupSchema,
    onSubmit: (values, actions) => dispatch(handleSubmit(values, actions)),
  });

  return <>
    <IndexNavbar/>
    <div className='d-flex flex-column h-100'>
      <div className='container-fluid h-100'>
        <div className='row justify-content-center align-content-center h-100'>
          <div className='col-md-6'>
            <div className='card shadow-sm'>
              <div className='card-body row p-5'>
                <div className='col-12 col-md-6 d-flex align-items-center justify-content-center'>
                  <link rel="apple-touch-icon" href="%PUBLIC_URL%/logo192.png" />
                </div>
                <FormikProvider value={formik}>
                  <Form onSubmit={formik.handleSubmit}>
                      <h1 className="text-center mb-4">Зарегистрироваться</h1>

                      <Form.Group className="mb-3">
                      <Form.Label htmlFor="username">Ваш ник</Form.Label>
                        <Form.Control type="text"
                          placeholder="Ваш ник"
                          autoComplete="username"
                          id="username"
                          onChange={formik.handleChange}
                          value={formik.values.username}
                          />
                      <ErrorMessage name="username" />
                    </Form.Group>

                    <Form.Group className="mb-3" >
                      <Form.Label htmlFor="password">Пароль</Form.Label>
                      <Form.Control type="password"
                        placeholder="Пароль"
                        id="password"
                        autoComplete="password"
                        onChange={formik.handleChange}
                        value={formik.values.password} />
                      <ErrorMessage name="password" />
                    </Form.Group>

                    <Form.Group className="mb-3" >
                      <Form.Label htmlFor="passwordConfirmation">Подтвердите пароль</Form.Label>
                      <Form.Control type="password"
                        placeholder="Подтвердите пароль"
                        id="passwordConfirmation"
                        autoComplete="passwordConfirmation"
                        onChange={formik.handleChange}
                        value={formik.values.passwordConfirmation} />
                      <ErrorMessage name="passwordConfirmation" />
                    </Form.Group>

                    <Button type="submit" disabled={isLoading}>
                      Зарегистрироваться
                    </Button>
                  </Form>
                </FormikProvider>
              </div>
          </div>
            <div className="card-footer p-4">
              <div className="text-center">
                <a href="/login">Залогиниться</a>
              </div>
            </div>
          </div>
        </div>
      </div>
  </div>
  </>
};

export default SignupPage;
