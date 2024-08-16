//TODO
// логика login
// карточки рядом
// запросы в отдельный файл в функции
// добавить Loading


import React, { useState, useEffect } from "react";
import FormData from 'form-data'
import axios from 'axios';
import routes from "../utils/routes.js";
import ImageCard from './ImageCard.jsx'
import { useDispatch, useSelector } from "react-redux";
import { setMemes } from "../slices/memesSlice";
import { getMemes, postMeme } from "../utils/requests.js";
import NavbarPage from "./Navbar.jsx";


const IndexPage = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedName, setSelectedName] = useState(null);

  const dispatch = useDispatch();
  const [loading, setLoading] = useState(true);

  const memes = useSelector((state) => state.memes.memes);
  const access_token = localStorage.getItem('user')

  useEffect(() => {
    const inner = async () => {
      try {
        const response = await getMemes(access_token)
        console.log('getMemes response', response)
        dispatch(setMemes(response.data))
      } catch (e) {
        console.log('memes get error');
        console.log(e)
      }      
    }
    inner();
  }, []);
  
  return (
    <>
    <NavbarPage/>
    <div className="container h-100 p-5 my-4 overflow-hidden rounded shadow">
      <div className="row h-100 bg-white flex-md-row">
        <form onSubmit={ async (event) => {
              event.preventDefault();
              try {
                const form = new FormData();
                form.append('file', selectedImage);
                form.append('filename', selectedName);
                const postMemeResponse = await postMeme(form, access_token);
                console.log('postMemeResponse', postMemeResponse);
                const getMemesResponse = await getMemes(access_token);
                console.log('getMemesResponse', getMemesResponse)
                dispatch(setMemes(getMemesResponse.data))
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
        {memes.map((meme) => {
          return <div key={meme.id}>
                  <ImageCard meme={meme}/>
                </div>
          }
        )}
    </>}
  </>
  );
}

export default IndexPage;