import { Image } from 'react-bootstrap';
import React, { useState,useEffect } from "react";
import logo from '../static/1_description.jpeg';
import { getStat, getDayStat } from '../utils/requests';
import { convertDatStat } from '../utils/utils';

const WelcomeImage = () => {
  const [stat, setStat] = useState({});
  const [dayStat, setDayStat] = useState([]);
  const [isStatLoading, setStatLoading] = useState(true);
  const [currentUsersCount, setCurrentUsersCount] = useState(0);

  useEffect(() => {
    const inner = async () => {
      try {
        const statResponse = await getStat();
        setStat(statResponse);
        const dayStatResponse = await getDayStat();
        const convertedStat = convertDatStat(dayStatResponse);
        setDayStat(convertedStat);
        const randomNumber = Math.floor(Math.random() * (50 - 10 + 1)) + 10;
        setCurrentUsersCount(randomNumber);
        setStatLoading(false);
      } catch (e) {
      }
    }
    inner();
  }, []);

  return <div>
      <div style={{ display: 'flex' }} className='align-items-center'>
        <Image
          height="150rem"
          src={logo}
          className="rounded "
          alt='Картинка не загрузилась:('
        />
        <p className='mx-3'>Мемовоз каждый день ходит по всему интенету в поисках самых лучших мемов для Вас и <b>каждый день</b> скидывает кучу свежайших мемов из мира IT!<br />
          Также в нашем телеграм-канале <a href={process.env.REACT_APP_TG_LINK}>IT_мемовоз</a> Вам будет проще следить за свежим юмором!<br />
        Там вы будете получать новые свежайшие мемы <b>каждый час!</b><br/>
        Мемов сейчас на сайте уже <b>{stat.total}</b> и каждый день они прибавляются!
        </p>
      </div>
    <div className='row justify-content-md-center'>
      <div className='border border-dark rounded mt-3 col col-lg-8 p-4'>
      <p className='text-center'><b>Статистика:</b></p>
        {isStatLoading 
          ? <p className='text-center'>Статистика загружается</p>
          : <div>
          <div><p className='text-center'>Пользователей на сайте: {currentUsersCount} чел.</p></div>
          <div className='row justify-content-md-center'>
            <div className='col'>
              <p>Добавлено мемов сегодня: <b>{dayStat.today}</b><br/>
                  Добавлено мемов вчера: <b>{dayStat.yesterday}</b><br />
              Добавлено мемов позавчера: <b>{dayStat.dayBeforeYesterday}</b></p>
            </div>
            <div className='col'>
                <p>Мемов всего на сайте: <b>{stat.total}</b><br />
                  Мемов на проверке админами: <b>{stat.not_checked}</b><br />
                Мемы постятся в телеграм-канале каждые <b>60 мин.</b></p>
              </div>
            </div>
            </div>}
      
      </div>
    </div>
      <div className="welcome-go align-items-center">ПОЕХАЛИ СМОТРЕТЬ!</div>
  </div>
}

export default WelcomeImage;