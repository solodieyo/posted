from sqlalchemy import select

from app.src.infrastructure.db.models import Channel
from app.src.infrastructure.db.repositories import BaseRepository


class ChannelRepository(BaseRepository):

	async def add_user_channel(
		self,
		user_id: int,
		channel_id: int,
		channel_name: str,
	):
		pass

	async def get_users_channels(self, user_id):
		res = await self.session.execute(
			select(Channel).where(Channel.owner_channel_id == user_id)
		)
		return res.fetchall()