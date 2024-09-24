from aiogram import Router
from aiogram.types import CallbackQuery
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from app.src.bot.keyboards.post_keyboard import create_post_keyboard
from app.src.factory.callback_factory.emoji_callback import EmojiCallback
from app.src.infrastructure.db.models import User
from app.src.infrastructure.db.repositories import GeneralRepository

router = Router()


@router.callback_query(EmojiCallback.filter())
@inject
async def callback_emoji(
	callback: CallbackQuery,
	callback_data: EmojiCallback,
	repository: FromDishka[GeneralRepository],
	user: User
):
	reaction_buttons = await repository.reactions.add_user_reaction(
		user_id=user.id,
		post_id=callback_data.post_id,
		reaction_id=callback_data.reaction_id
	)
	url_buttons = await repository.post.get_url_buttons(post_id=callback_data.post_id)

	await callback.message.edit_reply_markup(
		reply_markup=create_post_keyboard(
			url_buttons=url_buttons,
			emoji_buttons=reaction_buttons,
		)
	)