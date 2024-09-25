from aiogram_dialog import DialogManager


async def getter_channel_name(
	dialog_manager: DialogManager,
	**_
):
	return {
		"channel_name": dialog_manager.dialog_data['channel_name']
	}


async def media_menu_getter(dialog_manager: DialogManager, **_):
	return {
		'has_media': dialog_manager.dialog_data.get('has_media', False),
		'hide_media': dialog_manager.dialog_data.get('hide_media', False)
	}
