from aiogram import Bot
from aiogram.types import Message
from aiogram_dialog.manager.message_manager import SEND_METHODS

from app.src.bot.keyboards.post_keyboard import create_post_keyboard
from app.src.bot.sender.new_message_modal import NewMessage
from app.src.factory.reaction_factory import create_reactions
from app.src.infrastructure.db.models import Post
from app.src.infrastructure.db.repositories import GeneralRepository


async def send_message(
	bot: Bot,
	post: Post,
	repository: GeneralRepository
) -> Message:
	reactions = create_reactions(
		emoji_buttons=post.emoji_buttons,
		post_id=post.id,
		channel_id=post.channel_id
	)
	keyboard = create_post_keyboard(
		emoji_buttons=reactions,
		url_buttons=post.url_buttons,
	)
	async with bot:
		message = await _send_message(
			bot=bot,
			new_message=NewMessage(
				chat_id=post.channel_id,
				text=post.text,
				reply_markup=keyboard,
				media_id=post.media_id,
				media_content_type=post.media_content_type,
				hide_media=post.hide_media,
				disable_notification=post.notification
			)
		)
	await repository.reactions.add_reactions(
		reactions=reactions,
		message_id=message.message_id
	)
	await repository.post.message_sent(post_id=post.id)
	return message


async def _send_message(bot: Bot, new_message: NewMessage) -> Message:
	if new_message.media_id:
		return await _send_media(bot, new_message)
	else:
		return await _send_text(bot, new_message)


async def _send_text(bot: Bot, new_message: NewMessage) -> Message:
	message = await bot.send_message(
		chat_id=new_message.chat_id,
		text=new_message.text,
		disable_notification=new_message.disable_notification,
		reply_markup=new_message.reply_markup,
		parse_mode=new_message.parse_mode,
	)

	if new_message.poll_tittle:
		await _send_poll(bot, new_message)

	return message


async def _send_poll(bot: Bot, new_message: NewMessage):
	await bot.send_poll(
		chat_id=new_message.chat_id,
		question=new_message.poll_tittle,
		options=new_message.poll_options
	)


async def _send_media(bot: Bot, new_message: NewMessage) -> Message:
	method = getattr(bot, SEND_METHODS[new_message.media_content_type], None)
	if not method:
		raise ValueError(f"ContentType {new_message.media_content_type} is not supported")
	message = await method(
		new_message.chat_id,
		new_message.media_id,
		caption=new_message.text,
		reply_markup=new_message.reply_markup,
		parse_mode=new_message.parse_mode,
		has_spoiler=new_message.hide_media
	)

	if new_message.poll_tittle:
		await _send_poll(bot, new_message)

	return message
