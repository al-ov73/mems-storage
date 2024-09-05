import { configureStore } from '@reduxjs/toolkit';
import memesReducer from './memesSlice.js';
import categoryReducer from './categoriesSlice.js';

export default configureStore({
  reducer: {
    memes: memesReducer,
    categories: categoryReducer,
  },
});
