from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.src.factory.callback_factory.emoji_callback import EmojiCallback
from app.src.infrastructure.db.models import Reaction


def create_post_keyboard(
	url_buttons: str | None,
	emoji_buttons: list[Reaction] | None,
):
	builder = InlineKeyboardBuilder()
	if url_buttons:
		for row in url_buttons.split('\n'):
			buttons = []
			for button in row.split(' | '):
				tittle, url = button.split(' - ')
				buttons.append(InlineKeyboardButton(text=tittle, url=url))
			builder.row(*buttons, width=len(buttons))

	if emoji_buttons:
		buttons = []
		for reaction in emoji_buttons:
			text = f'{reaction.emoji} - {reaction.count_reaction}' if reaction.count_reaction > 0 else reaction.emoji
			buttons.append(InlineKeyboardButton(
				text=text,
				callback_data=EmojiCallback(
					emoji=reaction.emoji,
					post_id=reaction.post_id,
					reaction_id=reaction.id
				).pack())
			)
		builder.row(*buttons, width=len(buttons))
	return builder.as_markup()
