from aiogram.types import Message


def get_file_id(message: Message):
	if message.photo:
		return message.photo[-1].file_id
	elif message.document:
		return message.document.file_id
	elif message.video:
		return message.video.file_id, message.video.file_name
	else:
		return None