import React, { useEffect } from 'react';

const YandexAd = ({ blockId, style = {} }) => {
  useEffect(() => {
    // Функция для загрузки рекламы
    const loadAd = () => {
      // Проверяем, что Ya существует
      if (window.Ya && window.Ya.Context) {
        window.Ya.Context.AdvManager.render({
          blockId: blockId,
          renderTo: `yandex-rtb-${blockId}`,
          async: true
        });
      }
    };

    // Проверяем, загружена ли уже библиотека Яндекс.Рекламы
    if (window.Ya && window.Ya.Context) {
      loadAd();
    } else {
      // Если библиотека еще не загружена - добавляем в очередь
      window.yaContextCb = window.yaContextCb || [];
      window.yaContextCb.push(loadAd);
      
      // Загружаем скрипт, если он еще не загружен
      if (!document.querySelector('script[src*="yandex.ru/ads/system/context.js"]')) {
        const script = document.createElement('script');
        script.src = 'https://yandex.ru/ads/system/context.js';
        script.async = true;
        document.head.appendChild(script);
      }
    }

    // Очистка при размонтировании компонента
    return () => {
      if (window.Ya && window.Ya.Context) {
        window.Ya.Context.AdvManager.destroy(`yandex-rtb-${blockId}`);
      }
    };
  }, [blockId]);

  return (
    <div 
      id={`yandex-rtb-${blockId}`}
      style={{
        minHeight: '250px',
        margin: '20px 0',
        ...style
      }}
    />
  );
};

export default YandexAd;