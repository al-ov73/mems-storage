import axios from 'axios';
import routes from './routes';

const getMemes = async (accessToken) => axios.get(routes.memesPath, {
  headers: {
    Authorization: `Bearer ${accessToken}`,
  },
});

const getMessages = async (accessToken) => {
  const response = await axios.get(routes.messagesPath, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
  return response.data;
};

const getCategories = async (accessToken) => {
  const response = await axios.get(`${routes.memesPath}/categories`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
  return response.data;
};

const loginUser = async (values) => {
  const params = new URLSearchParams();
  params.append('username', values.email);
  params.append('password', values.password);
  return axios.post(routes.loginPath, params);
};

const signupUser = async (values) => {
  const params = new URLSearchParams();
  params.append('username', values.username);
  params.append('password', values.password);
  return axios.post(routes.signupPath, params);
};

const postMeme = async (form, accessToken) => axios.post(routes.memesPath, form, {
  headers: {
    Authorization: `Bearer ${accessToken}`,
  },
});

const deleteMeme = async (id, accessToken) => axios.delete(`${routes.memesPath}/${id}`, {
  headers: {
    Authorization: `Bearer ${accessToken}`,
  },
});

const validateToken = async (accessToken) => {
  if (!accessToken) {
    return false;
  }
  try {
    const response = await axios.get(`${routes.validateTokenPath}/${accessToken}`);
    return response.status === 200;
  } catch (e) {
    console.log('validate error', e);
    return false;
  }
};

const postLabel = async (form, accessToken) => {
  return axios.post(routes.labelsPath, form, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })
};

export {
  getMemes,
  getMessages,
  getCategories,
  loginUser,
  postMeme,
  deleteMeme,
  signupUser,
  validateToken,
  postLabel,
};
