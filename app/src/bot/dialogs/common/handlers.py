from datetime import date, datetime

from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from babel.dates import format_datetime
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from taskiq_redis import RedisScheduleSource

from app.src.bot.dialogs.common.post_delay import schedule_post
from app.src.infrastructure.db.models import User
from app.src.infrastructure.db.repositories import GeneralRepository


async def on_notification_clicked(
	_,
	__,
	dialog_manager: DialogManager
):
	notification = dialog_manager.dialog_data.get('notification', False)
	dialog_manager.dialog_data['notification'] = not notification


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


async def on_show_calendar(
	_,
	__,
	dialog_manager: DialogManager
):
	dialog_manager.dialog_data['show_calendar'] = not dialog_manager.dialog_data.get('show_calendar', False)


@inject
async def on_no_confirm_user(
	_,
	__,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
):
	user: User = dialog_manager.middleware_data['user']
	user.skip_confirm_post = not user.skip_confirm_post
	await repository.user.skip_confirm_post(user_id=user.id)


@inject
async def on_confirm_delay_post(
	callback: CallbackQuery,
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
		bot=bot,
		chat_id=callback.from_user.id
	)

	await dialog_manager.done()
	await callback.message.delete()


async def get_delay_confirm_info(
	dialog_manager: DialogManager,
	user: User,
	**_
):
	selected_date_iso = datetime.fromisoformat(dialog_manager.dialog_data['selected_date'])
	selected_date = format_datetime(selected_date_iso, "d MMMM Y г H:mm", locale='ru')
	return {
		"channel_name": dialog_manager.dialog_data['channel_name'],
		"selected_date": selected_date,
		'user_confirm': user.skip_confirm_post
	}


async def on_delay_click(
	_,
	__,
	dialog_manager: DialogManager
):
	dialog_manager.dialog_data['shifted_date'] = 0