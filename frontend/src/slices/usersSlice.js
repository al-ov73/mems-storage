import { createSlice } from '@reduxjs/toolkit'
// import { PayloadAction } from '@reduxjs/toolkit'
// import { User } from '../../app/services/auth'
// import { RootState } from '../../app/store'

const initialState = {
  access_token: null,
}

const slice = createSlice({
  name: 'auth',
  initialState,
  reducers: {

    setCredentials: (state, {payload: { access_token }}) => {
      state.access_token = access_token;
    },

    removeCredentials: (state) => {
      state.access_token = null;
    },
  },
})

export const { setCredentials, removeCredentials } = slice.actions

export default slice.reducer

export const selectCurrentUser = (state) => state.auth.username