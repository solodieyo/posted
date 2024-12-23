from dataclasses import dataclass

import pytz
from sqlalchemy import URL

LOCALES_PATH = r'C:\Users\solo\PycharmProjects\posted\app\translations'
CONFIG_PATH = r"config.toml"
moscow_tz = pytz.timezone('Europe/Moscow')


@dataclass
class Tg:
	token: str
	admin_id: int
	locales_path: str = LOCALES_PATH


@dataclass
class Postgres:
	database: str
	user: str
	password: str
	host: str
	port: int

	def build_dsn(self) -> URL:
		return URL.create(
			drivername="postgresql+asyncpg",
			username=self.user,
			password=self.password,
			host=self.host,
			port=self.port,
			database=self.database,
		)


@dataclass
class Redis:
	host: str
	port: int


@dataclass
class AppConfig:
	tg: Tg
	postgres: Postgres
	redis: Redis
