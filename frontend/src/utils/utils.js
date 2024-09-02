import { jwtDecode } from "jwt-decode";


const getUsernameFromStorage = () => {
  const token = localStorage.getItem('user')
  const tokenData = jwtDecode(token);
  const username = tokenData.username;
  return username;
};

const getUserIdFromStorage = () => {
  const token = localStorage.getItem('user')
  const tokenData = jwtDecode(token);
  const userId = tokenData.id;
  return userId;
};

export { getUsernameFromStorage, getUserIdFromStorage };