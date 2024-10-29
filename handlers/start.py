from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from kb import generator

router = Router()

@router.message(CommandStart())
async def start_cmd(msg: Message):
    await msg.answer(
        text='Hello, I am weather forecast bot! Press /get_weather to start!',
        reply_markup=generator.generate_kb(['/get_weather'])
    )
