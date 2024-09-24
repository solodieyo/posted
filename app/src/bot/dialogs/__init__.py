from aiogram import Router

from .add_channel_dialog.dialog import add_channel_dialog
from .create_post_dialog.dialog import create_post_dialog
from .main_menu_dialog.dialog import main_dialog


def include_dialogs():
	router = Router()
	router.include_routers(
		add_channel_dialog,
		create_post_dialog,
		main_dialog,
	)
	return router