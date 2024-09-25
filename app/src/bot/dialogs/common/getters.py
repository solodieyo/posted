from datetime import timedelta, datetime

from aiogram_dialog import DialogManager
from babel.dates import format_date
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.src.bot.utils.get_text import get_delay_text
from app.src.config.app_config import moscow_tz
from app.src.infrastructure.db.models import User, Channel
from app.src.infrastructure.db.repositories import GeneralRepository


@inject
async def create_post_getter(
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	user: User,
	**_
):
	channels: list[Channel] = await repository.channel.get_users_channels(user_id=user.id)
	if len(channels) == 1:
		dialog_manager.dialog_data.update(
			channel_id=channels[0].id,
			channel_name=channels[0].channel_name,
			channel_username=channels[0].channel_username,
			channel_tg_id=channels[0].channel_id
		)
		return {
			"one_channel": True,
			"channel_name": channels[0].channel_name
		}
	return {
		'channels': channels,
		'one_channel': True if len(channels) == 1 else False,
	}


def channel_itemgetter(channel: Channel) -> int:
	return channel.id


async def manage_menu_getter(dialog_manager: DialogManager, **_):
	return {
		'notification': dialog_manager.dialog_data.get('notification', False),
		'post_text': dialog_manager.dialog_data.get('post_text', '...')
	}


@inject
async def get_post_delay_text(
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	**_
):
	shift_days = dialog_manager.dialog_data.get('shifted_date', 0)
	selected_date = dialog_manager.dialog_data.get('selected_date')
	if not selected_date:
		selected_date = datetime.now(tz=moscow_tz) + timedelta(days=shift_days)
	else:
		selected_date = datetime.fromisoformat(selected_date)
	posts = await repository.post.get_post_per_date(
		channel_id=dialog_manager.dialog_data['channel_id'],
		date=selected_date,
	)

	scheduled_posts_text = ''
	if posts:
		for post in posts:
			scheduled_posts_text += f'<code>{post.scheduled_at.strftime("%H:%M")}</code> {post.text[:10]}\n'
		scheduled_posts_text += '\n'

	text = get_delay_text(
			scheduled_text=scheduled_posts_text,
			post_date=selected_date,
			count_post=len(posts) if len(posts) >= 1 else "ни одного поста",
			wrong_date=dialog_manager.dialog_data.get('wrong_date', False)
		)
	return {
		"post_delay_text": text,
		'wrong_date': dialog_manager.dialog_data.get('wrong_date', False),
	}


async def get_calendar_state(dialog_manager: DialogManager, **_):
	return {
		'show_calendar': dialog_manager.dialog_data.get('show_calendar', True)
	}


async def get_buttons_dates(
	dialog_manager: DialogManager,
	**_,
):
	shifted_date = dialog_manager.dialog_data.get('shifted_date', 0)

	left_date = datetime.now() + timedelta(days=shifted_date - 1)
	current_date = datetime.now() + timedelta(days=shifted_date)
	right_date = datetime.now() + timedelta(days=shifted_date + 1)

	return {
		"left_date": format_date(left_date, format='EEE, d MMM', locale='ru'),
		"current_date": format_date(current_date, format='EEE, d MMM', locale='ru'),
		"right_date": format_date(right_date, format='EEE, d MMM', locale='ru')
	}