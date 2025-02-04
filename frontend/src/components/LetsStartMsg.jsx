import React, { useState, useEffect } from "react";


const LetsStartMsg = () => {
  const [isWidthScreen, setIsWidthScreen] = useState(true);
  // Функция для проверки ширины экрана
  const checkScreenSize = () => {
    if (window.innerWidth <= 768) {
      setIsWidthScreen(false);
    } else {
      setIsWidthScreen(true);
    }
  }

  useEffect(() => {
    checkScreenSize();
    window.addEventListener('resize', checkScreenSize);

    return () => {
      window.removeEventListener('resize', checkScreenSize);
    };
  }, []);

  if (isWidthScreen) {
  return <div>
    <div className="welcome-go align-items-center">ПОЕХАЛИ СМОТРЕТЬ!</div>
    <div className="welcome-go align-items-center">И не забывайте добавлять нас в закладки (CTRL+D)</div>
  </div>
  }
  return <div className="welcome-go welcome-go-small align-items-center">ПОЕХАЛИ СМОТРЕТЬ!</div>
}

export default LetsStartMsg;