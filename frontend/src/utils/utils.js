import { jwtDecode } from "jwt-decode";


const getUsernameFromStorage = () => {
  const token = localStorage.getItem('user')
  const tokenData = jwtDecode(token);
  const username = tokenData.sub;
  return username;
};

export { getUsernameFromStorage };