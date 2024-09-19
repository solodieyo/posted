from cgitb import reset

from sqlalchemy import select

from app.src.infrastructure.db.models import User
from app.src.infrastructure.db.repositories import BaseRepository


class UserRepository(BaseRepository):
	async def get_or_create_user(
		self,
		tg_user_id: int,
		username: str,
		full_name: str,

	):
		user = await self.session.scalar(select(User).where(User.tg_user_id == tg_user_id))

		if not user:
			user = User(
				tg_user_id=tg_user_id,
				username=username,
				full_name=full_name
			)
			self.session.add(user)
			await self.session.commit()

		return user
