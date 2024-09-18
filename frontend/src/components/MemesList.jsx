import ImageCard from './ImageCard.jsx'
import { useSelector } from "react-redux";
import Col from 'react-bootstrap/Col';


const MemesList = () => {
  const currentCategory = useSelector((state) => state.categories.currentCategory);
  let memes = useSelector((state) => state.memes.memes);
  if (!currentCategory) {
        return ''
  }
  
  memes = (currentCategory === 'ALL') ? 
          memes :
          memes.filter((meme) => meme.category === currentCategory)

  return memes.map((meme) => {
              return <Col xs={6} md={4} className="mx-4 my-1" key={meme.id}>
                      <ImageCard meme={meme}/>
                    </Col>
              }
      )
  }

export default MemesList;