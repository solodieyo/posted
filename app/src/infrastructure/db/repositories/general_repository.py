from sqlalchemy.ext.asyncio import AsyncSession

from app.src.infrastructure.db.repositories import BaseRepository
from app.src.infrastructure.db.repositories.channel_repository import ChannelRepository
from app.src.infrastructure.db.repositories.post_repository import PostRepository
from app.src.infrastructure.db.repositories.reactions_repository import ReactionsRepository
from app.src.infrastructure.db.repositories.user_repository import UserRepository


class GeneralRepository(BaseRepository):
	def __init__(self, session: AsyncSession) -> None:
		super().__init__(session=session)
		self.user = UserRepository(session=session)
		self.channel = ChannelRepository(session=session)
		self.post = PostRepository(session=session)
		self.reactions = ReactionsRepository(session=session)
