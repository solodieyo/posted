from aiogram import Bot
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from app.src.bot.states.dialog_states import CreatePostStates
from app.src.bot.utils.message_misc import get_file_info, FileInfo
from app.src.infrastructure.db.maker.post_maker import create_post
from app.src.infrastructure.db.models.posts import Post
from app.src.infrastructure.db.repositories import GeneralRepository


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
	file_info: FileInfo = get_file_info(message)
	dialog_manager.dialog_data.update(
		has_media=True,
		media_file_id=file_info.file_id,
		media_content_type=file_info.content_type
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
	dialog_manager.dialog_data['media_content_type'] = None


async def input_url_buttons(
	message: Message,
	__,
	dialog_manager: DialogManager
):
	dialog_manager.dialog_data['url_buttons'] = message.text
	await dialog_manager.switch_to(state=CreatePostStates.post_manage_menu)


async def input_emoji_buttons(message: Message, __, dialog_manager: DialogManager):
	dialog_manager.dialog_data['emoji_buttons'] = message.text
	await dialog_manager.switch_to(state=CreatePostStates.post_manage_menu)


async def input_poll_tittle(message: Message, __, dialog_manager: DialogManager):
	dialog_manager.dialog_data['poll_tittle'] = message.text
	await dialog_manager.switch_to(state=CreatePostStates.post_manage_menu)


async def input_poll_choices(message: Message, __, dialog_manager: DialogManager):
	dialog_manager.dialog_data['poll_choices'] = message.text
	await dialog_manager.switch_to(state=CreatePostStates.post_manage_menu)


@inject
async def post_confirm(
	_,
	__,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	bot: FromDishka[Bot]
):
	post = create_post(
		data=dialog_manager.dialog_data,
		user_id=dialog_manager.event.from_user.id
	)

	await repository.post.create_post(post=post)

