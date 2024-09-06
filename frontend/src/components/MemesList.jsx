import React, { useState, useEffect } from "react";
import ImageCard from './ImageCard.jsx'
import { useDispatch, useSelector } from "react-redux";
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { setMemes } from "../slices/memesSlice";

import { getMemes, postMeme, getCategories } from "../utils/requests.js";
import NavbarPage from "./Navbar.jsx";
import MemeCreateForm from "./MemeCreateForm.jsx";
import CategoryCard from "./CategoryCard.jsx";
import { setCategories, setCurrentCategory } from "../slices/categoriesSlice.js";

const MemesList = () => {
  const currentCategory = useSelector((state) => state.categories.currentCategory);
  let memes = useSelector((state) => state.memes.memes);
  if (!currentCategory) {
        return ''
  }
  
  memes = (currentCategory === 'ALL') ? 
          memes :
          memes.filter((meme) => meme.category === currentCategory)

  return memes.map((meme) => {
              return <Col xs={6} md={4} className="mx-4 my-1" key={meme.id}>
                      <ImageCard meme={meme}/>
                    </Col>
              }
      )
  }

export default MemesList;