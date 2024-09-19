from app.src.infrastructure.db.models.posts import Post
from app.src.infrastructure.db.repositories import BaseRepository


class PostRepository(BaseRepository):
	async def create_post(self, post: Post):
		self.session.add(Post)
		await self.session.commit()