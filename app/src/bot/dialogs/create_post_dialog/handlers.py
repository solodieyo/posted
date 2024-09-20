from datetime import date, datetime, timedelta

from aiogram import Bot
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from taskiq_redis import RedisScheduleSource

from app.src.bot.dialogs.common.post_delay import schedule_post
from app.src.bot.states.dialog_states import CreatePostStates
from app.src.bot.utils.message_misc import get_file_info, FileInfo
from app.src.bot.utils.parse_time import parse_user_time
from app.src.infrastructure.db.maker.post_maker import create_post
from app.src.infrastructure.db.models import User
from app.src.infrastructure.db.repositories import GeneralRepository


async def on_select_channel(
	_,
	__,
	dialog_manager: DialogManager,
	selected_item: int
):
	dialog_manager.dialog_data['channel_id'] = selected_item
	await dialog_manager.switch_to(state=CreatePostStates.create_post)


async def input_post_text(
	message: Message,
	widget: MessageInput,
	dialog_manager: DialogManager
):
	dialog_manager.dialog_data['post_text'] = message.text
	await dialog_manager.switch_to(state=CreatePostStates.post_manage_menu)


async def on_notification_clicked(
	_,
	__,
	dialog_manager: DialogManager
):
	notification = dialog_manager.dialog_data.get('notification', True),
	dialog_manager.dialog_data['notification'] = not notification


async def input_post_media(
	message: Message,
	__,
	dialog_manager: DialogManager
):
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
	dialog_manager.dialog_data['url_buttons'] = message.text
	await dialog_manager.switch_to(state=CreatePostStates.post_manage_menu)


async def input_emoji_buttons(message: Message, __, dialog_manager: DialogManager):
	dialog_manager.dialog_data['emoji_buttons'] = message.text
	await dialog_manager.switch_to(state=CreatePostStates.post_manage_menu)


async def input_poll_tittle(message: Message, __, dialog_manager: DialogManager):
	dialog_manager.dialog_data['poll_tittle'] = message.text
	await dialog_manager.switch_to(state=CreatePostStates.post_manage_menu)


async def input_poll_choices(message: Message, __, dialog_manager: DialogManager):
	dialog_manager.dialog_data['poll_choices'] = message.text
	await dialog_manager.switch_to(state=CreatePostStates.post_manage_menu)


@inject
async def post_confirm(
	_,
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


async def on_show_calendar(
	_,
	__,
	dialog_manager: DialogManager
):
	dialog_manager.dialog_data['show_calendar'] = not dialog_manager.dialog_data.get('show_calendar', False)


@inject
async def input_time_delay(
	message: Message,
	__,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	redis_source: FromDishka[RedisScheduleSource],
	bot: FromDishka[Bot]
):
	user: User = dialog_manager.middleware_data['user']

	shifted_date = dialog_manager.dialog_data.get('shifted_date', 0)
	selected_date = dialog_manager.dialog_data.get('selected_date', datetime.now() + timedelta(days=shifted_date))

	parsed_date = parse_user_time(
		default_date=selected_date,
		time_string=message.text
	)

	if parsed_date:
		dialog_manager.dialog_data['wrong_date'] = False
		dialog_manager.dialog_data['selected_date'] = parsed_date
		if user.skip_confirm_post:
			await schedule_post(
				data=dialog_manager.dialog_data,
				user_id=dialog_manager.middleware_data['user'].id,
				repository=repository,
				redis_source=redis_source,
				bot=bot
			)
			await dialog_manager.done()
			return
		else:
			await dialog_manager.switch_to(state=CreatePostStates.post_delay_confirm)
			return
	dialog_manager.dialog_data['wrong_date'] = True


async def on_date_selected(
	_,
	__,
	dialog_manager: DialogManager,
	selected_date: date
):
	dialog_manager.dialog_data['selected_date'] = selected_date


async def shift_left_date(
	_,
	__,
	dialog_manager: DialogManager
):
	dialog_manager.dialog_data['shifted_date'] -= 1


async def shift_right_date(
	_,
	__,
	dialog_manager: DialogManager
):
	dialog_manager.dialog_data['shifted_date'] += 1


async def on_no_confirm_user(
	_,
	__,
	dialog_manager: DialogManager
):
	user: User = dialog_manager.middleware_data['user']
	user.skip_confirm_post = not user.skip_confirm_post


@inject
async def on_confirm_delay_post(
	_,
	__,
	dialog_manager: DialogManager,
	redis_source: FromDishka[RedisScheduleSource],
	repository: FromDishka[GeneralRepository],
	bot: FromDishka[Bot]
):
	await schedule_post(
		data=dialog_manager.dialog_data,
		user_id=dialog_manager.middleware_data['user'].id,
		repository=repository,
		redis_source=redis_source,
		bot=bot
	)

	await dialog_manager.done()
