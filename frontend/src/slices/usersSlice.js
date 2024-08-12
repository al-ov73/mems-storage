import { createSlice } from '@reduxjs/toolkit'
// import { PayloadAction } from '@reduxjs/toolkit'
// import { User } from '../../app/services/auth'
// import { RootState } from '../../app/store'

const initialState = {
  username: null,
  token: null,
}

const slice = createSlice({
  name: 'auth',
  initialState,
  reducers: {

    setCredentials: (state, {payload: { username, token }}) => {
      state.username = username;
      state.token = token;
    },

    removeCredentials: (state) => {
      state.username = null;
      state.token = null;
    },
  },
})

export const { setCredentials, removeCredentials } = slice.actions

export default slice.reducer

export const selectCurrentUser = (state) => state.auth.username