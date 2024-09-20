from typing import Union

from sqlalchemy import select

from app.src.infrastructure.db.models import Channel
from app.src.infrastructure.db.repositories import BaseRepository


class ChannelRepository(BaseRepository):

	async def add_user_channel(
		self,
		user_id: int,
		channel_id: int,
		channel_name: str,
		channel_username: str | None
	):
		channel = Channel(
			owner_channel_id=user_id,
			channel_id=channel_id,
			channel_name=channel_name,
			channel_username=channel_username
		)
		self.session.add(channel)
		await self.session.commit()

	async def get_users_channels(self, user_id):
		res = await self.session.execute(
			select(Channel).where(Channel.owner_channel_id == user_id)
		)
		return res.fetchall()

	async def exists_channels_user(self, user_id):
		res: Union[Channel, None] = await self.session.scalar(
			select(Channel).where(Channel.owner_channel_id == user_id)
		)
		if res:
			return True
		return False