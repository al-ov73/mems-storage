import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  memes: [],
}

const slice = createSlice({
  name: 'memes',
  initialState,
  reducers: {
    setMemes: (state, {payload}) => {
      state.memes = payload;
    },
  },
})

export const { setMemes } = slice.actions

export default slice.reducer