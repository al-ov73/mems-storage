import React from 'react';
import Button from 'react-bootstrap/Button';
import Figure from 'react-bootstrap/Figure';
import { useDispatch } from "react-redux";
import config from '../../config/config.js';
import { setCurrentCategory } from '../../slices/categoriesSlice.js';


const CategoryCard = ({ category })  => {
  const dispatch = useDispatch();

  const categoryName = category in config.categories ? config.categories[category].label : category
  const categoryLink = category in config.categories ? config.categories[category].coverLink : 'category-other.jpg'

  const categoryHandler = () => {
    dispatch(setCurrentCategory(category));
  };
  
  return (
    <>
      <Figure className="text-center">
      <img className="img-responsive"
          src={require(`../../static/categoryImages/${categoryLink}`)}
          alt="Картинка не загрузилась :("
          width="100"
          height="100"/>

        <Figure.Caption>
          <Button
            variant="primary"
            onClick={categoryHandler}>
            {categoryName}
          </Button>
        </Figure.Caption>
      </Figure>
    </>
  );
}

export default CategoryCard;