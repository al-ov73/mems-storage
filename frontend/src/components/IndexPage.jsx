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
import MemesList from "./MemesList.jsx";

const IndexPage = () => {
  const [createFormShow, setCreateFormShow] = useState(false);
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


  const categories = useSelector((state) => state.categories.categories);
  const memes = useSelector((state) => state.memes.memes);
  const access_token = localStorage.getItem('user')



  return (
    <>
    <NavbarPage/>
    <Button variant="outline-success" onClick={() => setCreateFormShow(true)}>Добавить мем</Button>
    <MemeCreateForm
        show={createFormShow}
        onHide={() => setCreateFormShow(false)}
      />
    <Container>
    <Row>
      {categories && <>
          <Button variant="outline-success" onClick={() => dispatch(setCurrentCategory('ALL'))}>Все мемы</Button>
          {categories.map((category) => {
            return <Col md={3} className="mx-4 my-1" key={category}>
                    <CategoryCard category={category}/>
                  </Col>
                }
              )}
          </>}
      </Row>
      <Row>
        <MemesList/>
      </Row>
    </Container>
  </>
  );
}

export default IndexPage;