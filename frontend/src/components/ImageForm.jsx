import React, { useState, useEffect } from "react";
import FormData from 'form-data'
import axios from 'axios';

const apiUrl = process.env.REACT_APP_API_URL;

const ImageForm = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedName, setSelectedName] = useState(null);
  const [memesList, setMemesList] = useState([]);
  const [linksList, setLinksList] = useState([]);

  useEffect(() => {
    axios.get(apiUrl).then((response) => {
      if (response.data !== memesList) {
        setMemesList(response.data)
      }
    })
  }, []);

  useEffect(() => {
    const promises = memesList.map((meme) => {
      return axios.get(`${apiUrl}/${meme.id}`).then((response) => {
        return {
          'link': response.data,
          'id': meme.id,
        }
      })
    })
    Promise.all(promises).then((meme_links) => setLinksList(meme_links))
  }, [memesList]);

  const handleImageDelete = async (id) => {
    axios.delete(`${apiUrl}/${id}`)
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
                console.log('selectedName', selectedName)
                axios.post(apiUrl, form, {
                  headers: {
                    'Content-Type': `multipart/form-data`,
                  }
                }).then((response) => {
                  console.log('frontend response', response)
                  axios.get(apiUrl).then((response) => {
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
                                      src={link.link}/>)}
    </>}
  </>
  );
}

export default ImageForm;