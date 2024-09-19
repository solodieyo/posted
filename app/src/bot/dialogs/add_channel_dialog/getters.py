from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.src.infrastructure.db.models import Channel
from app.src.infrastructure.db.repositories import GeneralRepository


@inject
async def create_post_getter(
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository]
	, **_
):
	channels: list[Channel] = await repository.channel.get_users_channels()

	return {
		'channels': channels,
		'one_channel': True if len(channels) == 1 else False
	}


def channel_itemgetter(channel: Channel) -> int:
	return channel.id


async def manage_menu_getter(dialog_manager: DialogManager):
	return {
		'notification': dialog_manager.dialog_data.get('notification', True),
		'post_text': dialog_manager.dialog_data.get('post_text', '...')
	}


async def media_menu_getter(dialog_manager: DialogManager):
	return {
		'has_media': dialog_manager.dialog_data.get('has_media', False),
		'hide_media': dialog_manager.dialog_data.get('hide_media', False)
	}