import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  categories: [],
  currentCategory: '',
}

const slice = createSlice({
  name: 'categories',
  initialState,
  reducers: {
    setCategories: (state, {payload}) => {
      state.categories = payload;
    },
    setCurrentCategory: (state, {payload}) => {
      state.currentCategory = payload;
    },
  },
})

export const { setCategories, setCurrentCategory } = slice.actions

export default slice.reducer