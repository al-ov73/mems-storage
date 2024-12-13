import { jwtDecode } from 'jwt-decode';

const getUsernameFromStorage = () => {
  // const token = localStorage.getItem('user');
  // const tokenData = jwtDecode(token);
  // const { username } = tokenData;
  return 'user';
};

const getUserIdFromStorage = () => {
  // const token = localStorage.getItem('user');
  // const tokenData = jwtDecode(token);
  // const userId = tokenData.id;
  return '1';
};

const convertDateTime = (isoString) => {
  const formatedDate= new Date(Date.parse(isoString));

  const seconds = formatedDate.getSeconds()
  const formatedSeconds = seconds < 10 ? `0${seconds}` : seconds

  const minutes = formatedDate.getMinutes()
  const formatedMinutes = minutes < 10 ? `0${minutes}` : minutes
  let time = `${formatedDate.getHours()}:${formatedMinutes}:${formatedSeconds}`;
  
  let date = `${formatedDate.toLocaleDateString("ru-RU")}`;
  const dateFormat = `${date}: ${time}`;
  return dateFormat;
}
export { getUsernameFromStorage, getUserIdFromStorage, convertDateTime };
