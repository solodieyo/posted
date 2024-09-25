from aiogram_dialog.widgets.kbd import Start, SwitchTo
from aiogram_dialog.widgets.text import Const

from app.src.bot.dialogs.common.widgets import I18NFormat
from app.src.bot.states.dialog_states import AddChannelStates, CreatePostStates, PollStates

NEW_CHANNEL = Start(
	I18NFormat('add-channel'),
	state=AddChannelStates.add_channel,
	id='__ADD_CHANNEL__'
)

BACK_TO_MANAGE_POST_MENU = SwitchTo(
	text=Const('🔙 Назад'),
	state=CreatePostStates.post_manage_menu,
	id='__BACK_TO_MANAGE_POST_MENU__'
)

BACK_TO_MANAGE_POLL_MENU = SwitchTo(
	state=PollStates.poll_manage_menu,
	text=Const('⬅️ Назад'),
	id='__BACK_TO_MANAGE_POLL_MENU__'
)
