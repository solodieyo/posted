from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from app.src.bot.states.dialog_states import CreatePostStates, AddChannelStates
from app.src.infrastructure.db.models import User
from app.src.infrastructure.db.repositories import GeneralRepository

router = Router()


@router.message(Command('create'))
@inject
async def create_command(
	message: Message,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	user: User
):
	user_have_channels = await repository.channel.get_users_channels(user_id=user.id)
	if user_have_channels:
		await dialog_manager.start(state=CreatePostStates.create_post, mode=StartMode.RESET_STACK)

	else:
		await dialog_manager.start(state=AddChannelStates.no_channel_yet, mode=StartMode.RESET_STACK)