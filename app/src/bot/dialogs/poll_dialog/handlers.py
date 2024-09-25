from datetime import timedelta, datetime

from aiogram import Bot
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from taskiq_redis import RedisScheduleSource

from app.src.bot.dialogs.common.post_delay import schedule_post
from app.src.bot.sender.send_message import send_message
from app.src.bot.states.dialog_states import PollStates
from app.src.bot.utils.parse_time import parse_user_time
from app.src.infrastructure.db.maker.post_maker import create_post
from app.src.infrastructure.db.models import User
from app.src.infrastructure.db.repositories import GeneralRepository


@inject
async def on_select_channel_poll(
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

	await dialog_manager.switch_to(state=PollStates.selected_channel)


async def input_tittle_text(
	message: Message,
	widget: MessageInput,
	dialog_manager: DialogManager
):
	channel_id = dialog_manager.dialog_data.get('channel_id')
	if not channel_id:
		await message.delete()
		return
	dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
	dialog_manager.dialog_data['poll_tittle'] = message.text
	await dialog_manager.switch_to(state=PollStates.change_poll_choices)


async def change_poll_tittle(message: Message, __, dialog_manager: DialogManager):
	dialog_manager.dialog_data['poll_tittle'] = message.text
	dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
	await dialog_manager.switch_to(state=PollStates.poll_manage_menu)


async def input_poll_choices(message: Message, __, dialog_manager: DialogManager):
	dialog_manager.dialog_data['poll_choices'] = message.text
	dialog_manager.show_mode = ShowMode.DELETE_AND_SEND
	await dialog_manager.switch_to(state=PollStates.poll_manage_menu)


@inject
async def poll_confirm(
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
	await send_message(bot=bot, repository=repository, post=post)


@inject
async def input_poll_time_delay(
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
				bot=bot,
				chat_id=dialog_manager.event.from_user.id
			)
			await dialog_manager.done()
			await message.delete()
			return
		else:
			await dialog_manager.switch_to(state=PollStates.poll_delay_confirm)
			return
	dialog_manager.dialog_data['wrong_date'] = True