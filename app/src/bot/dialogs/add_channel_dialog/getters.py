from aiogram_dialog import DialogManager


async def get_channel_name(dialog_manager: DialogManager, **_):
	return {
		"channel_name": dialog_manager.dialog_data.get("channel_name", None)
	}