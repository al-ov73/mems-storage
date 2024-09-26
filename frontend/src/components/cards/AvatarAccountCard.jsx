import Figure from 'react-bootstrap/Figure';

const AvatarAccounCard = ({ link })  => {

  return (
    <>
      <Figure className="text-center">
        <img className="img-responsive"
            src={link}
            alt="Картинка не загрузилась :("
            width="100"
            height="100"/>
      </Figure>
    </>
  );
}

export default AvatarAccounCard;