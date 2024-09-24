import Card from 'react-bootstrap/Card';
import Spinner from 'react-bootstrap/Spinner';

function IndexPageSpinner() {
  return <div align="center" className="position-absolute top-50 start-50 translate-middle">
    <h4>Ваши любимые мемы загружаются</h4>
    <h5>Пожалуйста подождите</h5>
    <Spinner animation="border" variant="primary" />
  </div>
}

export default IndexPageSpinner;