from aiogram_dialog import DialogManager


async def getter_poll_choices(dialog_manager: DialogManager, **_):
	return {
		"poll_choices": dialog_manager.dialog_data.get('poll_choices', ''),
		'poll_tittle': dialog_manager.dialog_data.get('poll_tittle', '.'),
		'notification': dialog_manager.dialog_data.get('notification', False),
	}