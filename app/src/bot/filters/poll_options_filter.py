from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram_dialog import DialogManager


class PollOptionsFilter(BaseFilter):
	async def __call__(self, message: Message, dialog_manager: DialogManager) -> bool:
		if len(message.text.split(',')) < 2:
			dialog_manager.dialog_data['wrong_options'] = True
			return False
		dialog_manager.dialog_data['wrong_options'] = False
		return True