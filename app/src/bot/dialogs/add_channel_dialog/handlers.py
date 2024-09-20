from aiogram import Bot
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.src.bot.states.dialog_states import AddChannelStates
from app.src.infrastructure.db.models import User
from app.src.infrastructure.db.repositories import GeneralRepository


@inject
async def check_channel_permissions(
	message: Message,
	__,
	dialog_manager: DialogManager,
	bot: FromDishka[Bot],
	repository: FromDishka[GeneralRepository],
):
	try:
		chat = message.forward_from
		permissions = await bot.get_chat_member(
			chat_id=chat.id,
			user_id=bot.id
		)
		await repository.channel.add_user_channel(
			channel_id=chat.id,
			channel_name=chat.first_name,
			channel_username=chat.username,
			user_id=dialog_manager.middleware_data['user'].id
		)
		dialog_manager.dialog_data['channel_name'] = chat.first_name
		await dialog_manager.switch_to(AddChannelStates.channel_linked)
	except:
		# обработать ошибку + добавить логику ошибки
		pass


