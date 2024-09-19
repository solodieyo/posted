from app.src.infrastructure.db.models.posts import Post


def create_post(data: dict, user_id: int) -> Post:
	return Post(
		channel_id=data['channel_id'],
		owner_user_id=user_id,
		text=data.get('post_text', '.'),
		notification=data.get('notification', True),
		media_id=data.get('media_id', None),
		url_buttons=data.get('url_buttons', None),
		emoji_buttons=data.get('emoji_buttons', None),
		poll_tittle=data.get('poll_tittle', None),
		poll_options=data.get('poll_options', None),
		scheduled=False,
		scheduled_at=None,
		hide_media=data.get('hide_media', False),
		media_content_type=data.get('media_content_type', None)
	)