from datetime import datetime

from aiogram import Bot
from taskiq.scheduler.created_schedule import CreatedSchedule
from taskiq_redis import RedisScheduleSource

from app.src.infrastructure.db.maker.post_maker import create_post
from app.src.infrastructure.db.repositories import GeneralRepository
from app.src.infrastructure.scheduler.tasks import delay_post, delay_poll


async def schedule_post(
	redis_source: RedisScheduleSource,
	repository: GeneralRepository,
	data: dict,
	user_id: int,
	bot: Bot,
	chat_id: int
):
	delay_time = datetime.fromisoformat(data['selected_date'])
	post = create_post(
		data=data,
		user_id=user_id,
		sent=False,
		scheduled=True,
		scheduled_at=delay_time
	)
	await repository.post.create_post(post=post)

	if post.poll_tittle:
		await delay_poll.schedule_by_time(
			source=redis_source,
			time=delay_time,
			post_id=post.id
		)
	else:
		await delay_post.schedule_by_time(
			source=redis_source,
			time=delay_time,
			post_id=post.id,
		)
	await bot.send_message(
		chat_id=chat_id,
		text=(f'✅ Публикация в канале <a href="t.me/{data["channel_username"]}">{data["channel_name"]}</a> '
			  f'Запланирована на  -  <code>{post.scheduled_at.strftime("%H:%M")}</code>')
	)
