from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseStorage, DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from dishka import AsyncContainer, make_async_container, Provider, Scope, from_context, provide

from app.src.bot.handlers import setup_routers
from app.src.config import AppConfig
from app.src.config.load_config import load_config
from app.src.factory.setup_middlewares import _setup_outer_middlewares
from app.src.infrastructure.di.bot import BotProvider
from app.src.infrastructure.di.db import DbProvider


def create_dishka(config: AppConfig) -> AsyncContainer:
	container = make_async_container(*get_providers(), context={AppConfig: config})
	return container


def get_providers():
	return [
		BotProvider(),
		DbProvider(),
	]


class DpProvider(Provider):
	scope = Scope.APP

	config = from_context(provides=AppConfig, scope=Scope.APP)

	@provide
	async def get_dispatcher(
		self,
		dishka: AsyncContainer,
		storage: BaseStorage,
		config: AppConfig,
	) -> Dispatcher:
		dp = Dispatcher(storage=storage)
		dp.include_routers(setup_routers())
		_setup_outer_middlewares(
			dishka=dishka,
			dispatcher=dp,
			config=config
		)
		return dp

	@provide(scope=Scope.APP)
	def get_redis(self, config: AppConfig) -> Redis:
		return Redis(
			host=config.redis.host,
			port=config.redis.port,
			decode_responses=True
		)

	@provide(scope=Scope.APP)
	def get_storage(self, redis: Redis) -> BaseStorage:
		return RedisStorage(
			redis=redis,
			key_builder=DefaultKeyBuilder(
				with_destiny=True,
				with_bot_id=True
			)
		)


def get_config() -> AppConfig:
	return load_config(AppConfig)


def get_dishka(config: AppConfig) -> AsyncContainer:
	return create_dishka(config)