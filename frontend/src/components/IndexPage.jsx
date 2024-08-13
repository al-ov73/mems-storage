//TODO
// изменения в контейнере без пересборки
// refresh token
// карточки рядом
// запросы в отдельный файл в функции
// добавить Loading


import React, { useState, useEffect } from "react";
import FormData from 'form-data'
import axios from 'axios';
import routes from "../routes/routes";
import ImageCard from './ImageCard.jsx'
import { useDispatch, useSelector } from "react-redux";
import { setMemes } from "../slices/memesSlice";


const IndexPage = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedName, setSelectedName] = useState(null);

  const dispatch = useDispatch();
  const [loading, setLoading] = useState(true);

  const memes = useSelector((state) => state.memes.memes);
  console.log('memes', memes)
  const access_token = localStorage.getItem('user')

  useEffect(() => {
    axios.get(routes.memesPath, {
      headers: {
        Authorization: `Bearer ${access_token}`,
      },
    })
      .then((response) => {
        dispatch(setMemes(response.data))
      })
      .catch((e) => {
        console.log('memes get error');
        console.log(e)
      })
  }, []);
  
  return (
    <>
    <div className="container h-100 p-5 my-4 overflow-hidden rounded shadow">
      <div className="row h-100 bg-white flex-md-row">
        <form onSubmit={ async (event) => {
              event.preventDefault();
              try {
                const form = new FormData();
                form.append('file', selectedImage);
                form.append('filename', selectedName);
                axios.post(routes.memesPath, form, {
                    headers: {
                      Authorization: `Bearer ${access_token}`,
                    }
                  })
                  .then((response) => console.log('frontend response', response))
                  .then(() => axios.get(routes.memesPath, {
                    headers: {
                      Authorization: `Bearer ${access_token}`,
                    },
                  })
                  .then((response) => dispatch(setMemes(response.data))))
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
      </div>
    </div>

    {memes && <>
        {memes.map((meme) => <ImageCard meme={meme}/>)}
    </>}
  </>
  );
}

export default IndexPage;