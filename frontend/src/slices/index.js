import { configureStore } from '@reduxjs/toolkit';
import usersReducer from './usersSlice.js';

export default configureStore({
  reducer: {
    users: usersReducer,
  },
});
