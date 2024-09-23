from aiogram import Bot
from dishka import FromDishka

from app.src.bot.sender.send_message import send_message
from app.src.infrastructure.db.models import Post
from app.src.infrastructure.db.repositories import GeneralRepository
from app.src.infrastructure.scheduler.broker import broker


@broker.task
async def delay_post(
	post_id: int,
	repository: FromDishka[GeneralRepository],
	bot: FromDishka[Bot]
):
	post: Post = await repository.post.get_post_by_id(post_id=post_id)
	async with bot:
		await send_message(
			bot=bot,
			post=post,
			repository=repository
		)