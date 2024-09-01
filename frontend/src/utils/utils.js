import { jwtDecode } from "jwt-decode";


const getUsernameFromStorage = () => {
  const token = localStorage.getItem('user')
  const tokenData = jwtDecode(token);
  console.log('tokenData',tokenData)
  const username = tokenData.username;
  return username;
};

export { getUsernameFromStorage };