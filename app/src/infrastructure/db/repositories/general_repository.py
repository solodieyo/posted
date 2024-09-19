from sqlalchemy.ext.asyncio import AsyncSession

from app.src.infrastructure.db.repositories import UserRepository, ChannelRepository
from app.src.infrastructure.db.repositories.post_repository import PostRepository


class GeneralRepository:
	def __init__(self, session: AsyncSession) -> None:
		super().__init__(session=session)
		self.user = UserRepository(session=session)
		self.channel = ChannelRepository(session=session)
		self.post = PostRepository(session=session)