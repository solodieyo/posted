from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from app.src.bot.states.dialog_states import MainMenuState, CreatePostStates

main_window = Window(
	Const('🏠 Главное меню'),
	Start(
		text=Const('Создать пост'),
		id='create_post',
		state=CreatePostStates.create_post
	),
	state=MainMenuState.main_menu
)

main_dialog = Dialog(
	main_window
)
