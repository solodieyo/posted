from datetime import date

from aiogram import Bot
from taskiq_redis import RedisScheduleSource

from app.src.infrastructure.db.maker.post_maker import create_post
from app.src.infrastructure.db.repositories import GeneralRepository
from app.src.infrastructure.scheduler.tasks import delay_post


async def schedule_post(
	redis_source: RedisScheduleSource,
	repository: GeneralRepository,
	data: dict,
	user_id: int,
	bot: Bot

):
	post = create_post(
		data=data,
		user_id=user_id,
		sent=False,
		scheduled=True,
		scheduled_at=data['selected_date']
	)

	await repository.post.create_post(post=post)

	await delay_post.schedule_by_time(
		redis_source=redis_source,
		scheduled_at=post.scheduled_at,
		post_id=post.id
	)

	await bot.send_message(
		chat_id=post.channel_id,
		text=(f'✅ Публикация в канале "<a href="t.me/{data["channel_username"]}">{data["channel_title"]}</a> '
		f'<code>{post.scheduled_at.strftime("%H:%M")}</code>')
	)
