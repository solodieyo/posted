from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager

from app.src.bot.states.dialog_states import MainMenuState

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, dialog_manager: DialogManager):
	await dialog_manager.start(state=MainMenuState.main_menu)

