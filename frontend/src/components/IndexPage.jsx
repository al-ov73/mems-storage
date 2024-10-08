import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { setMemes } from "../slices/memesSlice";
import { getMemes, getCategories } from "../utils/requests.js";
import NavbarPage from "./Navbar.jsx";
import { setCategories } from "../slices/categoriesSlice.js";
import MemesList from "./MemesList.jsx";
import CategoryCard from "./cards/CategoryCard.jsx";

const IndexPage = () => {
  const dispatch = useDispatch();

  // get categories
  useEffect(() => {
    const inner = async () => {
      const response = await getCategories(access_token)
      dispatch(setCategories(response));
    }
    inner();
  }, [])

  // get memes
  useEffect(() => {
    const inner = async () => {
      try {
        const response = await getMemes(access_token)
        dispatch(setMemes(response.data))
      } catch (e) {
        console.log('memes get error');
        console.log(e)
      }      
    }
    inner();
  }, []);

  const categories = useSelector((state) => state.categories.categories);
  const access_token = localStorage.getItem('user')

  return (
    <>
    <NavbarPage/>

    <Container>
    <Row xs="auto" className="justify-content-md-center my-4">

          <Col> <CategoryCard category={'ALL'}/></Col>
          {categories.map((category) => <Col key={category}><CategoryCard key={category} category={category}/></Col>)}

      </Row>
      <Row>
        <MemesList/>
      </Row>
    </Container>
  </>
  );
}

export default IndexPage;