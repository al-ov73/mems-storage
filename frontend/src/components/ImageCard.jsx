import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';

import axios from 'axios';
import routes from "../routes/routes";


const ImageCard = ({ meme })  => {
  const access_token = localStorage.getItem('user')

  const handleImageDelete = async (id) => {
    axios.delete(`${routes.memesPath}/${id}`, {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      }, { withCredentials: true })
      .then((response) => console.log(response))
  }
  return (
    <Card style={{ width: '18rem' }}>
      <Card.Img variant="top" src={meme.link} />
      <Card.Body>
        <Card.Title>{meme.name}</Card.Title>
        <Button variant="primary" onClick={() => handleImageDelete(meme.id)}>Удалить</Button>
      </Card.Body>
    </Card>
  );
}

export default ImageCard;