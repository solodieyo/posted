from sqlalchemy import select, and_, func, update

from app.src.infrastructure.db.models import Post
from app.src.infrastructure.db.repositories import BaseRepository


class PostRepository(BaseRepository):

	async def create_post(self, post: Post):
		self.session.add(post)
		await self.session.commit()

	async def get_post_per_date(self, channel_id, date):
		posts = await self.session.scalars(
			select(Post)
			.where(
				and_(
					Post.channel_id == channel_id,
					func.date(Post.scheduled_at) == date
				)
			)
		)
		return posts

	async def get_post_by_id(self, post_id):
		post: Post = await self.session.scalar(
			select(Post)
			.where(Post.id == post_id)
		)
		return post

	async def message_sent(self, post_id):
		await self.session.execute(
			update(Post)
			.where(Post.id == post_id)
			.values(sent=True)
		)

	async def get_url_buttons(self, post_id):
		result = await self.session.execute(
			select(Post.url_buttons).where(Post.id == post_id)
		)
		return result.fetchone()