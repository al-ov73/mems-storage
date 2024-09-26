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

const signupUser = async (values, photo) => {
  const form = new FormData();
  form.append('username', values.username);
  form.append('password', values.password);
  form.append('first_name', values.first_name);
  form.append('last_name', values.last_name);
  form.append('file', photo || '');
  return axios.post(routes.signupPath, form);
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

const postComment = async (form, accessToken) => {
  return axios.post(routes.commentsPath, form, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })
};

const postLike = async (form, accessToken) => {
  return axios.post(routes.likesPath, form, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })
};

const delLike = async (likeId, accessToken) => {
  return axios.delete(`${routes.likesPath}/${likeId}`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })
};

const getComments = async (memeId, accessToken) => {
  const response = await axios.get(`${routes.commentsPath}/meme/${memeId}`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })
  return response.data;
};

const getLabelsNames = async (accessToken) => {
  const response = await axios.get(routes.labelsPath, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })
  const labels = response.data
  return labels.map((label) => label.title);
};

const getUser = async (userId, accessToken) => {
  const response = await axios.get(`${routes.usersPath}/${userId}`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })
  return response.data;
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
  postComment,
  postLike,
  delLike,
  getComments,
  getLabelsNames,
  getUser,
};
