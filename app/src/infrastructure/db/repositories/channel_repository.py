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

	async def get_users_channels(self, user_id: int):
		res = await self.session.scalars(
			select(Channel).where(Channel.owner_channel_id == user_id)
		)
		return res.all()

	async def exists_channels_user(self, user_id: int):
		res: Union[Channel, None] = await self.session.scalar(
			select(Channel).where(Channel.owner_channel_id == user_id)
		)
		if res:
			return True
		return False

	async def get_chanel_by_id(self, channel_id: int):
		result: Channel = await self.session.scalar(
			select(Channel).where(Channel.id == channel_id)
		)
		return result

	async def get_channel_by_tg_id(self, channel_tg_id: int):
		result: Channel = await self.session.scalar(
			select(Channel).where(Channel.channel_id == channel_tg_id)
		)
		return result
