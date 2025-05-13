from aiogram import Router
from aiogram.types import BufferedInputFile, Message
from aiogram.utils.chat_action import ChatActionSender

from ...config.config import bot
from ...utils.gigachat import get_response_from_gigachat

gigachat_router = Router()


@gigachat_router.message()
async def other_command(message: Message) -> None:
    print(f"get message: '{message}'")
    giga_reply = await get_response_from_gigachat(message.text)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        if giga_reply.image:
            image = BufferedInputFile(giga_reply.image, filename="giga.jpg")
            await message.reply_photo(image)
            return
        await message.reply(giga_reply.text_reply)
