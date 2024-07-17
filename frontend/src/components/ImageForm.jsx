import React, { useState } from "react";
import FormData from 'form-data'
import axios from 'axios';

const imagePostUrl = 'http://127.0.0.1:8000'
const imageGetUrl = 'http://127.0.0.1:8000'

const ImageForm = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedName, setSelectedName] = useState(null);
  
  const handleObjectsList = async () => {
    axios.get(imageGetUrl).then((response) => console.log(response))
  }
  return (
    <div className="container h-100 p-5 my-4 overflow-hidden rounded shadow">
    <div className="row h-100 bg-white flex-md-row">


      <form onSubmit={ async (event) => {
            event.preventDefault();
            try {
              let file = new FormData();
              file.append('file', selectedImage, selectedName);
              axios.post(imagePostUrl, file, {
                headers: {
                  'Content-Type': `multipart/form-data`,
                }
              }).then((response) => console.log('frontend response', response))              
            } catch (error) {
              console.log('error->', error)
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
        </div>
        <div className="form-group">
        <label >приложите картинку</label>
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
      <button className="btn btn-primary" type="button" onClick={handleObjectsList}>
          Получить список файлов
      </button>
    </div>
    </div>


  );
}

export default ImageForm;