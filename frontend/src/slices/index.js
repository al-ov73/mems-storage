import { configureStore } from '@reduxjs/toolkit';
import memesReducer from './memesSlice.js';

export default configureStore({
  reducer: {
    memes: memesReducer,
  },
});
