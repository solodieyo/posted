from aiogram.filters import BaseFilter
from aiogram.types import Message


class ForwardFilter(BaseFilter):

	async def __call__(self, message: Message):
		if message.forward_origin:
			return True
		return False