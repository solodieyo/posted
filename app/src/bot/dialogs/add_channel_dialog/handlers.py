from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from app.src.bot.states.dialog_states import CreatePostStates
from app.src.bot.utils.message_misc import get_file_id


async def on_select_channel(
	_,
	__,
	dialog_manager: DialogManager,
	selected_item: int
):
	dialog_manager.dialog_data['channel_id'] = selected_item
	await dialog_manager.switch_to(state=CreatePostStates.create_post)


async def input_post_text(
	message: Message,
	widget: MessageInput,
	dialog_manager: DialogManager
):
	dialog_manager.dialog_data['post_text'] = message.text
	await dialog_manager.switch_to(state=CreatePostStates.post_manage_menu)


async def on_notification_clicked(
	_,
	__,
	dialog_manager: DialogManager
):
	notification = dialog_manager.dialog_data.get('notification', True),
	dialog_manager.dialog_data['notification'] = not notification


async def input_post_media(
	message: Message,
	__,
	dialog_manager: DialogManager
):
	dialog_manager.dialog_data.update(
		has_media=True,
		media_file_id=get_file_id(message)
	)


async def on_hide_media(
	_,
	__,
	dialog_manager: DialogManager
):
	dialog_manager.dialog_data['hide_media'] = not dialog_manager.dialog_data.get('hide_media', False)


async def on_delete_media(
	_,
	__,
	dialog_manager: DialogManager
):
	dialog_manager.dialog_data['has_media'] = False					
	dialog_manager.dialog_data['media_file_id'] = None


async def input_url_buttons(Там сегодняшнее какой-то кол-во времени записало и все отвал.
	message: Message,
	__,
	dialog_manager: DialogManager
):
	dialog_manager.dialog_data['url_buttons'] = message.text
	await dialog_manager.switch_to(state=CreatePostStates.post_manage_menu)