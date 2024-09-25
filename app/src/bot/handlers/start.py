from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from app.src.bot.states.dialog_states import MainMenuState

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
	await message.delete()
	await message.answer(
		text='<b>Создание поста</b> - /create_post\n\n'
			 '<b>Создание голосования</b> - /create_poll\n',
	)

