import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Image from 'react-bootstrap/Image';
import Figure from 'react-bootstrap/Figure';
import { useDispatch, useSelector } from "react-redux";
import config from '../config/config';
import { setCategories, setCurrentCategory } from "../slices/categoriesSlice.js";


const CategoryCard = ({ category })  => {
  const dispatch = useDispatch();

  const categoryName = category in config.categories ? config.categories[category].label : category
  const categoryLink = category in config.categories ? config.categories[category].coverLink : ''

  const categoryHandler = () => {
    dispatch(setCurrentCategory(category));
  };
  
  return (
    <>
      <Figure className="text-center">
      <img className="img-responsive"
          src={require(`../static/categoryImages/${categoryLink}`)}
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