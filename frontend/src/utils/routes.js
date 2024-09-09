const apiPath = process.env.REACT_APP_API_URL;


export default {
  loginPath: `${apiPath}/auth/jwt/login`,
  signupPath: `${apiPath}/auth/jwt/signup`,
  validateTokenPath: `${apiPath}/auth/jwt/validate_token`,
  usersPath: `${apiPath}/users`,
  memesPath: `${apiPath}/memes`,
  chatPath: `${apiPath}/chat`,
  messagesPath: `${apiPath}/chat/messages`,
  apiStatic: `${apiPath}/static`,
}
