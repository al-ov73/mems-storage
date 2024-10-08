import React from 'react';
import { Button } from "react-bootstrap"
import { getMemes, postLike, delLike } from "../utils/requests";
import FormData from 'form-data'
import { getUserIdFromStorage } from "../utils/utils";
import { setMemes } from "../slices/memesSlice";
import { useDispatch } from "react-redux";
import HeartComponent from "./Heart";

const LikeButton = ({meme}) => {
  const dispatch = useDispatch();
  const access_token = localStorage.getItem('user');
  const userId = getUserIdFromStorage();

  let userLike = meme.likes.find((like) => like.author_id === userId)
  const buttonVariant = userLike ? "danger" : "outline-danger"

  const likeHandler = async () => {
    if (userLike) {
      await delLike(userLike.id, access_token);
    } else {
      const form = new FormData();
      form.append('meme_id', meme.id);
      await postLike(form, access_token);
    }
    const getMemesResponse = await getMemes(access_token);
    dispatch(setMemes(getMemesResponse.data))
  }

  return <>
    <Button 
          variant={buttonVariant}
          onClick={likeHandler}>
    {meme.likes.length > 0 && meme.likes.length} <HeartComponent/> Нравится
    </Button>
  </>
}

export default LikeButton;