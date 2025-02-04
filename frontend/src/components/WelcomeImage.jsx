import { Image } from 'react-bootstrap';
import React, { useState,useEffect } from "react";
import logo from '../static/1_description.jpeg';
import { getStat } from '../utils/requests';


const WelcomeImage = () => {
  const [stat, setStat] = useState({});


  useEffect(() => {
    const inner = async () => {
      try {
        const statResponse = await getStat();
        setStat(statResponse);
      } catch (e) {
      }
    }
    inner();
  }, []);

  return <div style={{ display: 'flex' }} className='align-items-center'>
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
}

export default WelcomeImage;