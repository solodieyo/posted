from aiogram.filters.callback_data import CallbackData


class EmojiCallback(CallbackData, prefix="ej"):
	post_id: int
	reaction_id: int