from asyncio import run

from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from dishka.integrations.aiogram import setup_dishka

from app.src.factory.main_factory import get_config, get_dishka
from app.src.factory.setup_log import setup_logging


async def main():
	setup_logging()
	config = get_config()
	dishka = get_dishka(config)

	bot: Bot = await dishka.get(Bot)
	dp: Dispatcher = await dishka.get(Dispatcher)
	setup_dialogs(dp)
	setup_dishka(container=dishka, router=dp)

	dp['dishka_container'] = dishka

	await bot.delete_webhook(drop_pending_updates=True)
	await dp.start_polling(bot)


if __name__ == '__main__':
	run(main())