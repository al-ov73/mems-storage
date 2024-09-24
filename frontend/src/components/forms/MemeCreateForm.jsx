import React, { useState, useEffect } from "react";
import FormData from 'form-data'
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { useDispatch } from "react-redux";

import { setMemes } from "../../slices/memesSlice.js";
import { getMemes, postMeme, getCategories } from "../../utils/requests.js";
import config from "../../config/config.js";
import Row from "react-bootstrap/esm/Row.js";
import Col from "react-bootstrap/esm/Col.js";


const MemeCreateForm = ({ show, onHide }) => {
    const [selectedImage, setSelectedImage] = useState(null);
    const [selectedName, setSelectedName] = useState(null);
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState(null);
    const dispatch = useDispatch();
    const access_token = localStorage.getItem('user')

    useEffect(() => {
        const inner = async () => {
          const response = await getCategories(access_token)
          console.log('categories response', response);
          setCategories(response);
        }
        inner();
      }, [])

    return <>
    <Modal
        show={show}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
    >
      <Form className="m-4" onSubmit={ async (event) => {
          event.preventDefault();
          try {
            const form = new FormData();
            form.append('file', selectedImage);
            form.append('filename', selectedName);
            form.append('category', selectedCategory);
            console.log('selectedCategory', selectedCategory)
            const postMemeResponse = await postMeme(form, access_token);
            console.log('postMemeResponse', postMemeResponse);
            const getMemesResponse = await getMemes(access_token);
            console.log('getMemesResponse', getMemesResponse)
            dispatch(setMemes(getMemesResponse.data))
            onHide();
          } catch (error) {
            console.log('error->', error)
            onHide();
          }
        }}>
      <Form.Group>
        <Form.Label>
          <p className="fs-4">
            Загрузить новый мем
          </p>
        </Form.Label>
        <Form.Control
          className="my-3"
          placeholder="Введите имя"
          type="text"
          name="name"
          onChange={(event) => {
            setSelectedName(event.target.value);
          }}
        />
        <Form.Select
          className="my-3"
          aria-label="Выбор категории"
          onChange={(event) => {
            setSelectedCategory(event.target.value);
          }}>
          <option>Выберите категорию</option>
          {categories.map((frontendCategory) => {
            const calLabel = frontendCategory in config.categories ? config.categories[frontendCategory].label : frontendCategory
            return <option key={frontendCategory} value={frontendCategory}>{calLabel}</option>
          })}
        </Form.Select>
        
        <Form.Label className="mt-1">Приложите картинку</Form.Label>
        <Form.Control
        className="mb-3"
          type="file"
          name="file"
          onChange={(event) => {
            setSelectedImage(event.target.files[0]);
          }}
        />
      </Form.Group>
      <Row>
        <Col className="justify-content-md-center"><Button type="submit"> Загрузить файл </Button></Col>
        <Col className="justify-content-md-center"><Button onClick={onHide}>Закрыть</Button></Col>
      </Row>
    </Form>

  </Modal>
  </>
}

export default MemeCreateForm;