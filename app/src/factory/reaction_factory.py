from app.src.infrastructure.db.models import Reaction


def create_reactions(
	emoji_buttons: str,
	post_id: int,
	channel_id: int
) -> list[Reaction]:
	reactions = []
	for emoji in emoji_buttons.split(','):
		reaction = Reaction(
				emoji=emoji,
				post_id=post_id,
				channel_id=channel_id
			)
		reactions.append(reaction)
	return reactions