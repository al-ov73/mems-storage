import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Image from 'react-bootstrap/Image';
import config from '../config/config';

const CategoryCard = ({ category })  => {
  const categoryName = category in config.categories ? config.categories[category].label : category
  const categoryLink = category in config.categories ? config.categories[category].coverLink : ''

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
          <Button variant="primary">
            Посмотреть
          </Button>
        </Card.Body>
      </Card>
    </>
  );
}

export default CategoryCard;