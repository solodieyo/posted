from aiogram import F
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Start, Cancel
from aiogram_dialog.widgets.text import Const, Format

from app.src.bot.dialogs.add_channel_dialog.getters import get_channel_name
from app.src.bot.dialogs.add_channel_dialog.handlers import check_channel_permissions
from app.src.bot.dialogs.common.widgets import I18NFormat
from app.src.bot.filters.from_channel_filter import ForwardFilter
from app.src.bot.states.dialog_states import AddChannelStates, CreatePostStates

no_channel_yet = Window(
	Const(
		text='<b>Вы не добавили бота, или не дали ему права</b>\n',
		when=F['dialog_data']['no_permission_bot'].is_(True)
	),
	I18NFormat(
		text='no-channel-yet',
	),
	MessageInput(
		func=check_channel_permissions,
		filter=ForwardFilter()
	),
	state=AddChannelStates.no_channel_yet
)

channel_linked = Window(
	I18NFormat(
		text='channel-linked',
	),
	Start(
		text=Const('Новый пост'),
		state=CreatePostStates.create_post,
		id='create_post'
	),
	state=AddChannelStates.channel_linked,
	getter=get_channel_name
)

new_channel = Window(
	Const(
		text='<b>Вы не добавили бота, или не дали ему права</b>\n',
		when=F['dialog_data']['no_permission_bot'].is_(True)
	),
	Const(
		text='<b>Такой канал уже подключен</b>\n',
		when=F['dialog_data']['channel_exist'].is_(True)
	),
	I18NFormat(
		text='new-channel',
	),
	MessageInput(
		func=check_channel_permissions,
		filter=ForwardFilter()
	),
	Cancel(
		text=Const('Назад'),
	),
	state=AddChannelStates.add_channel,
)

add_channel_dialog = Dialog(
	no_channel_yet,
	channel_linked,
	new_channel
)
