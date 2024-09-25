from datetime import date, datetime, timedelta, tzinfo

import pytz
from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from taskiq_redis import RedisScheduleSource

from app.src.bot.dialogs.common.post_delay import schedule_post
from app.src.bot.enums.message_type import MessageType
from app.src.bot.sender.send_message import send_message
from app.src.bot.states.dialog_states import CreatePostStates
from app.src.bot.utils.message_misc import get_file_info, FileInfo
from app.src.bot.utils.parse_time import parse_user_time
from app.src.config.app_config import moscow_tz
from app.src.infrastructure.db.maker.post_maker import create_post
from app.src.infrastructure.db.models import User
from app.src.infrastructure.db.repositories import GeneralRepository


@inject
async def on_select_channel(
	_,
	__,
	dialog_manager: DialogManager,
	selected_item: int,
	repository: FromDishka[GeneralRepository]
):
	channel = await repository.channel.get_chanel_by_id(channel_id=selected_item)
	dialog_manager.dialog_data.update(
		channel_id=channel.id,
		channel_name=channel.channel_name,
		channel_username=channel.channel_username,
		channel_tg_id=channel.channel_id
	)

	await dialog_manager.switch_to(state=CreatePostStates.selected_channel)


async def input_post_text(
	message: Message,
	widget: MessageInput,
	dialog_manager: DialogManager
):
	channel_id = dialog_manager.dialog_data.get('channel_id')
	if not channel_id:
		await message.delete()
		return
	dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
	dialog_manager.dialog_data['post_text'] = message.text
	await dialog_manager.switch_to(state=CreatePostStates.post_manage_menu)


async def input_post_media(
	message: Message,
	__,
	dialog_manager: DialogManager
):
	dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
	file_info: FileInfo = get_file_info(message)
	dialog_manager.dialog_data.update(
		has_media=True,
		media_file_id=file_info.file_id,
		media_content_type=file_info.content_type
	)


async def on_hide_media(
	_,
	__,
	dialog_manager: DialogManager
):
	dialog_manager.dialog_data['hide_media'] = not dialog_manager.dialog_data.get('hide_media', False)


async def on_delete_media(
	_,
	__,
	dialog_manager: DialogManager
):
	dialog_manager.dialog_data['has_media'] = False
	dialog_manager.dialog_data['media_file_id'] = None
	dialog_manager.dialog_data['media_content_type'] = None


async def input_url_buttons(
	message: Message,
	__,
	dialog_manager: DialogManager
):
	dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
	dialog_manager.dialog_data['url_buttons'] = message.text
	await dialog_manager.switch_to(state=CreatePostStates.post_manage_menu)


async def input_emoji_buttons(message: Message, __, dialog_manager: DialogManager):
	dialog_manager.dialog_data['emoji_buttons'] = message.text
	dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
	await dialog_manager.switch_to(state=CreatePostStates.post_manage_menu)


@inject
async def post_confirm(
	callback: CallbackQuery,
	__,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	bot: FromDishka[Bot]
):
	post = create_post(
		data=dialog_manager.dialog_data,
		user_id=dialog_manager.middleware_data['user'].id,
	)
	await repository.post.create_post(post=post)
	await send_message(bot=bot, repository=repository, post=post)
	await dialog_manager.done()
	await callback.message.delete()
	await bot.send_message(chat_id=callback.from_user.id, text='✅ Пост опубликован')


@inject
async def input_time_delay(
	message: Message,
	__,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	redis_source: FromDishka[RedisScheduleSource],
	bot: FromDishka[Bot]
):
	dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
	user: User = dialog_manager.middleware_data['user']

	shifted_date = dialog_manager.dialog_data.get('shifted_date', 0)
	selected_date = dialog_manager.dialog_data.get('selected_date')
	if not selected_date:
		selected_date = datetime.now(tz=moscow_tz) + timedelta(days=shifted_date)
	else:
		selected_date = datetime.fromisoformat(selected_date)
	parsed_date = parse_user_time(
		default_date=selected_date,
		time_string=message.text
	)

	if parsed_date:
		dialog_manager.dialog_data['wrong_date'] = False
		dialog_manager.dialog_data['selected_date'] = parsed_date.isoformat()
		if user.skip_confirm_post:
			await schedule_post(
				data=dialog_manager.dialog_data,
				user_id=dialog_manager.middleware_data['user'].id,
				repository=repository,
				redis_source=redis_source,
				bot=bot,
				chat_id=dialog_manager.event.from_user.id
			)
			await dialog_manager.done()
			await message.delete()
			return
		else:
			await dialog_manager.switch_to(state=CreatePostStates.post_delay_confirm)
			return
	dialog_manager.dialog_data['wrong_date'] = True


async def insert_post_type(
	_,
	__,
	dialog_manager: DialogManager
):
	dialog_manager.dialog_data['post_type'] = MessageType.message