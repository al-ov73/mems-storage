import React, { useState } from 'react';
import axios from 'axios';
import './TelegramChat.css';

const TelegramChat = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [name, setName] = useState('');
    const [message, setMessage] = useState('');
    const [isSending, setIsSending] = useState(false);
    const [isSent, setIsSent] = useState(false);
    const [error, setError] = useState('');

    const BOT_TOKEN = process.env.REACT_APP_MEMOVOZ_BOT_API;
    const CHAT_ID = process.env.REACT_APP_ADMIN_API;

    const toggleChat = () => {
        setIsOpen(!isOpen);
        if (isOpen) {
            setError('');
            setIsSent(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!name.trim() || !message.trim()) {
            setError('Пожалуйста, заполните все поля');
            return;
        }

        setIsSending(true);
        setError('');

        try {
            const text = `Новое сообщение от ${name}:\n${message}`;
            console.log(text)
            await axios.post(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
                chat_id: CHAT_ID,
                text: text,
            });

            setIsSent(true);
            setName('');
            setMessage('');
            setTimeout(() => setIsSent(false), 3000);
        } catch (err) {
            setError('Ошибка при отправке сообщения. Попробуйте позже.');
            console.error('Telegram send error:', err);
        } finally {
            setIsSending(false);
        }
    };

    return (
        <div className={`telegram-chat ${isOpen ? 'open' : ''}`}>
            {isOpen ? (
                <div className="chat-window">
                    <div className="chat-header">
                        <h3>Написать сообщение</h3>
                        <button className="animated-button close-btn" onClick={toggleChat}>×</button>
                    </div>

                    <form onSubmit={handleSubmit} className="chat-form">
                        {error && <div className="error-message">{error}</div>}
                        {isSent && <div className="success-message">Сообщение отправлено!</div>}

                        <div className="form-group">
                            <label htmlFor="name">Ваше имя:</label>
                            <input
                                id="name"
                                type="text"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                disabled={isSending}
                                className="form-input"
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="message">Сообщение:</label>
                            <textarea
                                id="message"
                                value={message}
                                onChange={(e) => setMessage(e.target.value)}
                                disabled={isSending}
                                rows="4"
                                className="form-input"
                            />
                        </div>

                        <button
                            type="submit"
                            disabled={isSending}
                            className={`animated-button send-btn ${isSending ? 'sending' : ''}`}
                        >
                            {isSending ? 'Отправка...' : 'Отправить'}
                        </button>
                    </form>
                </div>
            ) : (
                <button className="animated-button chat-toggle-btn" onClick={toggleChat}>
                    Написать нам
                </button>
            )}
        </div>
    );
};

export default TelegramChat;