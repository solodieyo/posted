from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from app.src.bot.states.dialog_states import CreatePostStates

router = Router()


@router.message(Command('create'))
async def start_command(message: Message, dialog_manager: DialogManager):
	await dialog_manager.start(state=CreatePostStates.create_post)