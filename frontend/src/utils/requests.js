import axios from 'axios';
import routes from './routes';

const getMemes = async (access_token) => {
  return axios.get(routes.memesPath, {
      headers: {
        Authorization: `Bearer ${access_token}`,
      },
    })
}

const getMessages = async (access_token) => {
  const response = await axios.get(routes.messagesPath, {
      headers: {
        Authorization: `Bearer ${access_token}`,
      },
    })
  return response.data
}

const getCategories = async (access_token) => {
  const response = await axios.get(`${routes.memesPath}/categories`, {
      headers: {
        Authorization: `Bearer ${access_token}`,
      },
    })
  return response.data
}

const loginUser = async (values) => {
  const params = new URLSearchParams();
  params.append('username', values.email);
  params.append('password', values.password);
  return axios.post(routes.loginPath, params);  
}

const signupUser = async (values) => {
  const params = new URLSearchParams();
  params.append('username', values.username);
  params.append('password', values.password);
  return axios.post(routes.signupPath, params);
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
  })
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

export { getMemes, getMessages, getCategories, loginUser, postMeme, deleteMeme, signupUser, validateToken }