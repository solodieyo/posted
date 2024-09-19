from sqlalchemy.ext.asyncio import AsyncSession

from app.src.infrastructure.db.repositories import UserRepository, ChannelRepository


class GeneralRepository:
	def __init__(self, session: AsyncSession) -> None:
		super().__init__(session=session)
		self.user = UserRepository(session=session)
		self.channel = ChannelRepository(session=session)