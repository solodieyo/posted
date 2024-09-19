from multiprocessing.managers import State
from tkinter import Button

from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Start, Cancel

from app.src.bot.dialogs.common.widgets import I18NFormat
from app.src.bot.states.dialog_states import AddChannelStates, CreatePostStates

no_channel_yet = Window(
	I18NFormat(
		text='no-channel-yet',
	),
	MessageInput(
		func=,
	),
	state=AddChannelStates.no_channel_yet
)


channel_linked = Window(
	I18NFormat(
		text='channel-linked',
	),
	Start(
		text=I18NFormat('create-post'),
		state=CreatePostStates.create_post,
		id='create_post'
	),
	state=AddChannelStates.channel_linked
)

new_channel = Window(
	I18NFormat(
		text='new-channel',
	),
	MessageInput(
		func=,
	),
	Cancel(),
	state=AddChannelStates.add_channel
)