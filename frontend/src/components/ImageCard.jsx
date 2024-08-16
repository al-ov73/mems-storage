import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { deleteMeme } from '../utils/requests';


const ImageCard = ({ meme })  => {
  const access_token = localStorage.getItem('user')

  return (
    <Card style={{ width: '18rem' }}>
      <Card.Img variant="top" src={meme.link} alt='Картинка не загрузилась:('/>
      <Card.Body>
        <Card.Title>{meme.name}</Card.Title>
        <Button variant="primary"
                onClick={() => deleteMeme(meme.id, access_token)}>
          Удалить
        </Button>
      </Card.Body>
    </Card>
  );
}

export default ImageCard;