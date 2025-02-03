import React from 'react';

const BookmarkButton = () => {
    const addToBookmarks = () => {
        const url = window.location.href;
        const title = document.title;

        if (window.sidebar && window.sidebar.addPanel) {
            // Для Firefox
            window.sidebar.addPanel(title, url, '');
        } else if (window.external && ('AddFavorite' in window.external)) {
            // Для IE
            window.external.AddFavorite(url, title);
        } else if (window.opera && window.print) {
            // Для Opera
            const link = document.createElement('a');
            link.href = url;
            link.title = title;
            link.rel = 'sidebar';
            link.click();
        } else {
            // Для других браузеров (Chrome, Safari, Edge)
            alert(`Нажмите ${navigator.userAgent.toLowerCase().indexOf('mac') !== -1 ? 'Cmd+D' : 'Ctrl+D'} чтобы добавить страницу в закладки.`);
        }
    };

    return (
        <button className="mx-4 nav-button" onClick={addToBookmarks}>
            Добавить в закладки
        </button>
    );
};

export default BookmarkButton;