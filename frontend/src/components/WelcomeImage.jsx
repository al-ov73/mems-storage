import { Image } from 'react-bootstrap';
import logo from '../static/1_description.jpeg';

const WelcomeImage = () => {
    return <div style={{ display: 'flex'}} className='align-items-center'>
        <Image
            height="150rem"
            src={logo}
            className="rounded "
            alt='Картинка не загрузилась:('
        />
            <p className='mx-3 '>Мемовоз парсит весь интернет в поисках самых лучших мемов для Вас и <span className="fw-bold">каждый день</span> скидывает кучу свежайших мемов из мира IT!<br/>
Также в нашем телеграм-канале <a href={process.env.REACT_APP_TG_LINK}>IT_мемовоз</a> Вам будет проще следить за свежим юмором!<br/>
Там вы будете получать новые свежайшие мемы <b>каждый час!</b></p>

    </div>


}

export default WelcomeImage;