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

import CategoryCard from "./CategoryCard.jsx";
import { setCategories, setCurrentCategory } from "../slices/categoriesSlice.js";
import MemesList from "./MemesList.jsx";

const IndexPage = () => {

  const dispatch = useDispatch();

  // get categories
  useEffect(() => {
    const inner = async () => {
      const response = await getCategories(access_token)
      console.log('categories response', response);
      dispatch(setCategories(response));
    }
    inner();
  }, [])

  // get memes
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

  const currentCategory = useSelector((state) => state.categories.currentCategory);
  const categories = useSelector((state) => state.categories.categories);
  const memes = useSelector((state) => state.memes.memes);
  const access_token = localStorage.getItem('user')

  console.log('currentCategory->>', currentCategory)

  return (
    <>
    <NavbarPage/>

    <Container>
    <Row xs="auto" className="justify-content-md-center my-4">
      {currentCategory ?
          <Button variant="outline-success" onClick={() => dispatch(setCurrentCategory(''))}>Вернуться к выбору категории</Button>
          :
        <> 
          <Col> <CategoryCard category={'ALL'}/></Col>
          {categories.map((category) => <Col><CategoryCard key={category} category={category}/></Col>)}
        </>
      }
      </Row>
      <Row>
        <MemesList/>
      </Row>
    </Container>
  </>
  );
}

export default IndexPage;