from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_bot_commands(bot: Bot):
	commands = [
		BotCommand(command="create_post", description="Создать пост"),
		BotCommand(command="create_poll", description="Создать голосование"),
	]
	await bot.set_my_commands(
		commands=commands,
		scope=BotCommandScopeAllPrivateChats(),
		language_code='ru'
	)