import axios from 'axios';
import routes from './routes';
import { validateYupSchema } from 'formik';

const getMemes = async (access_token) => {
  return axios.get(routes.memesPath, {
      headers: {
        Authorization: `Bearer ${access_token}`,
      },
    })
}

const loginUser = async (values) => {
  const params = new URLSearchParams();
  params.append('username', values.email);
  params.append('password', values.password);
  return axios.post(routes.loginPath, params, { withCredentials: true });  
}

const signupUser = async (values) => {
  const params = new URLSearchParams();
  params.append('username', values.username);
  params.append('password', values.password);
  return axios.post(routes.signupPath, params, { withCredentials: true });
}

const postMeme = async (form, access_token) => {
  return axios.post(routes.memesPath, form, {
    headers: {
      Authorization: `Bearer ${access_token}`,
    }
  })
}

const deleteMeme = async (id, access_token) => {
  return axios.delete(`${routes.memesPath}/${id}`, {
    headers: {
      Authorization: `Bearer ${access_token}`,
    },
  }, { withCredentials: true })
}

const validateToken = async (access_token) => {
  if (!access_token) {
    return false;
  }
  try {
    const response = await axios.get(`${routes.validateTokenPath}/${access_token}`)
    return response.status === 200 ? true : false;
  } catch (e) {
    console.log('validate error', e);
    return false;
  }
}

export { getMemes, loginUser, postMeme, deleteMeme, signupUser, validateToken }