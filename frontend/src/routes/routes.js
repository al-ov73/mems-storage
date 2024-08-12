const apiPath = process.env.REACT_APP_API_URL;


export default {
  loginPath: `${apiPath}auth/jwt/login/`,
  signupPath: `${apiPath}auth/register/`,
  usersPath: `${apiPath}users/`,
  memesPath: `${apiPath}memes/`,
}
