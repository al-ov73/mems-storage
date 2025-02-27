from aiogram import Bot

async def send_reminder(bot: Bot, data: dict):
    user_id = data["user_id"]
    text = data['text']
    await bot.send_message(user_id, text) 