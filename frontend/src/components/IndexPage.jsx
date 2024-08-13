import React, { useState, useEffect } from "react";
import FormData from 'form-data'
import axios from 'axios';
import routes from "../routes/routes";
import { useSelector, useDispatch } from 'react-redux';


const IndexPage = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedName, setSelectedName] = useState(null);
  const [memesList, setMemesList] = useState([]);
  const [linksList, setLinksList] = useState([]);
  
  const access_token = localStorage.getItem('user')

  console.log('access_token', access_token)

  useEffect(() => {
    axios.get(routes.memesPath, {
      headers: {
        Authorization: `Bearer ${access_token}`,
      },
    })
      .then((response) => {
        if (response.data !== memesList) {
          setMemesList(response.data)
        }
      })
      .catch((e) => {
        console.log('memes get error');
        console.log(e)
      })
  }, []);
  
  useEffect(() => {
    const promises = memesList.map((meme) => {
      return axios.get(`${routes.memesPath}/${meme.id}`, {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      }, { withCredentials: true }).then((response) => {
        return {
          'link': response.data,
          'id': meme.id,
        }
      })
    })
    Promise.all(promises).then((meme_links) => setLinksList(meme_links))
  }, [memesList]);

  console.log('memesList', memesList)
  console.log('linksList', linksList)

  const handleImageDelete = async (id) => {
    axios.delete(`${routes.memesPath}/${id}`, { withCredentials: true })
      .then((response) => console.log(response))
  }

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
                    'Content-Type': `multipart/form-data`,
                  }
                }).then((response) => {
                  console.log('frontend response', response)
                  axios.get(routes.memesPath).then((response) => {
                    if (response.data !== memesList) {
                      setMemesList(response.data)
                    }
                  })
                })
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

    {linksList && <>
        {linksList.map((link) => <img key={link.id}
                                      onClick={() => handleImageDelete(link.id)}
                                      src={link.link.link}/>)}
    </>}
  </>
  );
}

export default IndexPage;