import { Button } from "react-bootstrap"
import { getMemes, postLike, delLike } from "../utils/requests";
import FormData from 'form-data'
import { getUserIdFromStorage } from "../utils/utils";
import { setMemes } from "../slices/memesSlice";
import { useDispatch } from "react-redux";

const LikeButton = ({meme}) => {
  const dispatch = useDispatch();
  const access_token = localStorage.getItem('user');
  const userId = getUserIdFromStorage();

  let userLike = meme.likes.find((like) => like.author_id === userId)
  const buttonVariant = userLike ? "danger" : "outline-danger"

  const likeHandler = async () => {
    if (userLike) {
      const response = await delLike(userLike.id, access_token);
      console.log('del like response', response)
    } else {
      const form = new FormData();
      form.append('meme_id', meme.id);
      const response = await postLike(form, access_token);
      console.log('like response', response)      
    }
    const getMemesResponse = await getMemes(access_token);
    dispatch(setMemes(getMemesResponse.data))
  }

  return <>
    <Button 
          variant={buttonVariant}
          onClick={likeHandler}>
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
        <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143q.09.083.176.171a3 3 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15"/>
      </svg> Нравится
    </Button>
  </>
}

export default LikeButton;