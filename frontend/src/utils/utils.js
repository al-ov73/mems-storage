import { jwtDecode } from 'jwt-decode';

const getUsernameFromStorage = () => {
  try {
    const token = localStorage.getItem('user');
    const tokenData = jwtDecode(token);
    const { username } = tokenData;
    return username;
  } catch (InvalidTokenError) {
    return null
  }
  
};

const getUserIdFromStorage = () => {
  try {
    const token = localStorage.getItem('user');
    const tokenData = jwtDecode(token);
    const userId = tokenData.id;
    return userId;
  } catch (InvalidTokenError) {
    return null
  }
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

const convertDatStat = (dayStat) => {
  let result = {
    "today": 0,
    "yesterday": 0,
    "dayBeforeYesterday": 0,
  }
  let today = new Date();
  let yesterday = new Date();
  yesterday.setDate(today.getDate() - 1);
  let dayBeforeYesterday = new Date();
  dayBeforeYesterday.setDate(today.getDate() - 2);
  
  for (let stat of dayStat) {
    const converted = new Date(stat.date)
    if (converted.toLocaleDateString() === today.toLocaleDateString()) {
      result.today = stat.count;
    } else if (converted.toLocaleDateString() === yesterday.toLocaleDateString()) {
      result.yesterday = stat.count;
    } else if (converted.toLocaleDateString() === dayBeforeYesterday.toLocaleDateString()) {
      result.dayBeforeYesterday = stat.count;
    }
  }
  return result;
}

export { getUsernameFromStorage, getUserIdFromStorage, convertDateTime, convertDatStat };
