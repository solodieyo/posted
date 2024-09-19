from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_post_keyboard(url_buttons: str, emoji_buttons: str, post_id):
	builder = InlineKeyboardBuilder()
	for row in url_buttons.split('\n'):
		buttons = []
		for button in row.split(' | '):
			tittle, url = button.split(' - ')
			buttons.append(InlineKeyboardButton(text=tittle, url=url))
		builder.row(*buttons, width=len(buttons))

	buttons = []
	for emoji in emoji_buttons.split(','):
		buttons.append(InlineKeyboardButton(text=emoji, callback_data=f"emoji_{emoji}_0"))

	builder.row(*buttons, width=len(buttons))
	return builder.as_markup()