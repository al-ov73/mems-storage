import React, { useState, useEffect } from "react";
import FormData from 'form-data'
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { useDispatch, useSelector } from "react-redux";

import { setMemes } from "../slices/memesSlice";
import { getMemes, postMeme, getCategories } from "../utils/requests.js";
import config from "../config/config.js";


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
    <form onSubmit={ async (event) => {
        event.preventDefault();
        try {
          const form = new FormData();
          form.append('file', selectedImage);
          form.append('filename', selectedName);
          form.append('category', selectedCategory);
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
  <div className="form-group">
    <label >Введите имя</label>
    <input
      className="form-control"
      type="text"
      name="name"
      onChange={(event) => {
        setSelectedName(event.target.value);
      }}
    />
        <Form.Select
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

    </div>
    <div className="form-group">
    <label>Приложите картинку</label>
    <input
      className="form-control"
      type="file"
      name="file"
      onChange={(event) => {
        setSelectedImage(event.target.files[0]);
      }}
    />
    </div>
    <button className="btn btn-primary" type="submit">
      Загрузить файл
    </button>
  </form>
  <Modal.Footer>
        <Button onClick={onHide}>Закрыть</Button>
</Modal.Footer>
  </Modal>
  </>
}

export default MemeCreateForm;