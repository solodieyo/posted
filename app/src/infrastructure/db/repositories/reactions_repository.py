from sqlalchemy import delete, and_, update, Result, select

from app.src.infrastructure.db.models import Reaction, UserReaction
from app.src.infrastructure.db.repositories import BaseRepository


class ReactionsRepository(BaseRepository):

	async def add_reactions(
		self,
		emoji_buttons: str,
		post_id: int,
		channel_id: int
	):
		reactions = []
		for emoji in emoji_buttons.split(','):
			reaction = Reaction(
				emoji=emoji,
				post_id=post_id,
				channel_id=channel_id
			)
			self.session.add(reaction)
			await self.session.flush()
			reactions.append(reaction)
		await self.session.commit()
		return reactions

	async def add_user_reaction(
		self,
		user_id: int,
		post_id: int,
		reaction_id: int
	):
		user_reaction = await self._get_user_reaction(
			user_id=user_id,
			post_id=post_id
		)

		if user_reaction:
			if user_reaction.reaction_id == reaction_id:
				await self._decrease_reaction_count(reaction_id)
				await self._delete_user_reaction(user_id, post_id, reaction_id)
				await self.session.commit()
			else:
				await self._change_reaction(
					user_reaction, reaction_id
				)
		else:
			await self._inscribe_reaction_count(reaction_id)

			user_reaction = UserReaction(
				user_id=user_id,
				reaction_id=reaction_id,
				post_id=post_id
			)
			self.session.add(user_reaction)
		await self.session.commit()
		reactions = await self.get_post_reactions(post_id=post_id)
		return reactions

	async def _get_user_reaction(self, user_id: int, post_id: int) -> UserReaction | None:
		return await self.session.scalar(
			select(UserReaction).where(
				UserReaction.user_id == user_id,
				UserReaction.post_id == post_id
			)
		)

	async def _decrease_reaction_count(self, reaction_id: int):
		await self.session.execute(
			update(Reaction)
			.where(Reaction.id == reaction_id)
			.values(count_reaction=Reaction.count_reaction - 1)
		)

	async def _inscribe_reaction_count(self, reaction_id: int):
		await self.session.execute(
			update(Reaction)
			.where(Reaction.id == reaction_id)
			.values(count_reaction=Reaction.count_reaction + 1)
		)

	async def _delete_user_reaction(self, user_id: int, post_id: int, reaction_id: int):
		await self.session.execute(
			delete(UserReaction)
			.where(
				UserReaction.user_id == user_id,
				UserReaction.post_id == post_id,
				UserReaction.reaction_id == reaction_id
			))

	async def _change_reaction(
		self,
		user_reaction: UserReaction,
		reaction_id: int
	):
		await self._decrease_reaction_count(user_reaction.reaction_id)
		await self._inscribe_reaction_count(reaction_id)
		await self.session.execute(
			update(UserReaction)
			.where(
				UserReaction.user_id == user_reaction.user_id,
				UserReaction.post_id == user_reaction.post_id
			)
			.values(reaction_id=reaction_id)
		)

	async def get_post_reactions(self, post_id: int):
		result = await self.session.scalars(
			select(Reaction).where(Reaction.post_id == post_id)
		)
		return result