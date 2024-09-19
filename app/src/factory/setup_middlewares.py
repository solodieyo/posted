from aiogram import Dispatcher
from dishka import AsyncContainer

from app.src.bot.midllwares.user_middleware import UserMiddleware
from app.src.config import AppConfig


def _setup_outer_middlewares(
	dispatcher: Dispatcher,
	dishka: AsyncContainer,
	config: AppConfig
) -> None:
	dispatcher.message.outer_middleware(UserMiddleware(dishka=dishka))
	dispatcher.callback_query.outer_middleware(UserMiddleware(dishka=dishka))
