import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Image from 'react-bootstrap/Image';
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
      <Card style={{ width: '18rem' }}>
        <Image 
                height="150rem"
                src={require(`../static/categoryImages/${categoryLink}`)}
                className="rounded mx-auto d-block"
                alt='Картинка не загрузилась:('
        />
        <Card.Body>
          <Card.Title>{categoryName}</Card.Title>
          <Button
            variant="primary"
            onClick={categoryHandler}>
            Посмотреть
          </Button>
        </Card.Body>
      </Card>
    </>
  );
}

export default CategoryCard;