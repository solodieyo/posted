from asyncio import run
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from dishka.integrations.aiogram import setup_dishka

from app.src.factory.main_factory import get_config, get_dishka
from app.src.factory.set_commands import set_bot_commands
from app.src.factory.setup_log import setup_logging
from app.src.infrastructure.scheduler.broker import broker


async def main():
	await broker.startup()
	setup_logging()
	config = get_config()
	dishka = get_dishka(config)

	bot: Bot = await dishka.get(Bot)
	dp: Dispatcher = await dishka.get(Dispatcher)
	await set_bot_commands(bot)
	setup_dialogs(dp)
	setup_dishka(container=dishka, router=dp)

	dp['dishka_container'] = dishka

	await bot.delete_webhook(drop_pending_updates=True)
	try:
		await dp.start_polling(bot)
	finally:
		await dishka.close()
		await broker.shutdown()


if __name__ == '__main__':
	with suppress(KeyboardInterrupt):
		run(main())