from aiogram import Dispatcher
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentCompileCore, FluentRuntimeCore
from dishka import AsyncContainer

from app.src.bot.midllwares.user_middleware import UserMiddleware
from app.src.config import AppConfig


def _setup_outer_middlewares(
	dispatcher: Dispatcher,
	dishka: AsyncContainer,
	config: AppConfig
) -> None:
	i18n_middleware = I18nMiddleware(
		core=FluentRuntimeCore(
				path=config.tg.locales_path,
			)
		)
	i18n_middleware.setup(dispatcher=dispatcher)
	dispatcher.message.outer_middleware(UserMiddleware(dishka=dishka))
	dispatcher.callback_query.outer_middleware(UserMiddleware(dishka=dishka))
