from aiogram import Bot
from dishka import FromDishka
from dishka.integrations.taskiq import inject

from app.src.bot.sender.send_message import send_message
from app.src.infrastructure.db.models import Post
from app.src.infrastructure.db.repositories import GeneralRepository
from app.src.infrastructure.scheduler.broker import broker


@broker.task
@inject
async def delay_post(
	post_id: int,
	repository: FromDishka[GeneralRepository],
	bot: FromDishka[Bot]
):
	await _delay(
		post_id=post_id,
		repository=repository,
		bot=bot
	)


@broker.task
@inject
async def delay_poll(
	post_id: int,
	repository: FromDishka[GeneralRepository],
	bot: FromDishka[Bot]
):
	await _delay(
		post_id=post_id,
		repository=repository,
		bot=bot
	)


async def _delay(
	post_id: int,
	repository: GeneralRepository,
	bot: Bot
):
	post: Post = await repository.post.get_post_by_id(post_id=post_id)
	async with bot:
		await send_message(
			bot=bot,
			post=post,
			repository=repository
		)
	await repository.post.message_sent(post_id=post_id)