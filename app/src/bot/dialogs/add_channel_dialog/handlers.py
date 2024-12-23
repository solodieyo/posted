from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.src.bot.states.dialog_states import AddChannelStates
from app.src.infrastructure.db.repositories import GeneralRepository


@inject
async def check_channel_permissions(
	message: Message,
	__,
	dialog_manager: DialogManager,
	bot: FromDishka[Bot],
	repository: FromDishka[GeneralRepository],
):
	dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
	try:
		chat = message.forward_origin.chat
		permissions = await bot.get_chat_member(
			chat_id=chat.id,
			user_id=bot.id
		)
		dialog_manager.dialog_data['no_permission_bot'] = None
		if await _check_channel_exist(repository=repository, channel_id=chat.id):
			dialog_manager.dialog_data['channel_exist'] = True
			return
		dialog_manager.dialog_data['channel_exist'] = None

		await repository.channel.add_user_channel(
			channel_id=chat.id,
			channel_name=chat.title,
			channel_username=chat.username,
			user_id=dialog_manager.middleware_data['user'].id
		)
		dialog_manager.dialog_data['channel_name'] = chat.title
		await dialog_manager.switch_to(AddChannelStates.channel_linked)
	except TelegramForbiddenError as e:
		dialog_manager.dialog_data['no_permission_bot'] = True


async def _check_channel_exist(repository: GeneralRepository, channel_id: int):
	channel = await repository.channel.get_channel_by_tg_id(channel_tg_id=channel_id)
	return bool(channel)