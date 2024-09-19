from aiogram_dialog.widgets.kbd import Start, SwitchTo
from aiogram_dialog.widgets.text import Const

from app.src.bot.dialogs.common.widgets import I18NFormat
from app.src.bot.states.dialog_states import AddChannelStates, CreatePostStates

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