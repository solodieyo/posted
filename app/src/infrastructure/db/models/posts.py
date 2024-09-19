from datetime import datetime
from typing import Optional

from aiogram.enums import ContentType
from aiogram_dialog.widgets.media import Media
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.src.infrastructure.db.models import Int64, Int16, Base


class Post(Base):
	__tablename__ = 'posts'

	id: Mapped[Int16] = mapped_column(primary_key=True, autoincrement=True)
	channel_id: Mapped[Int16] = mapped_column(ForeignKey('channels.id'), nullable=False)
	owner_user_id: Mapped[Int64] = mapped_column(ForeignKey('users.id'))
	text: Mapped[str] = mapped_column(nullable=False)
	media_id: Mapped[Optional[str]] = mapped_column(nullable=True)
	media_content_type: Mapped[Optional[ContentType]] = mapped_column(nullable=True)
	url_buttons: Mapped[Optional[str]] = mapped_column(nullable=True)
	emoji_buttons: Mapped[Optional[str]] = mapped_column(nullable=True)
	poll_tittle: Mapped[Optional[str]] = mapped_column(nullable=True)
	poll_options: Mapped[Optional[str]] = mapped_column(nullable=True)
	scheduled: Mapped[bool] = mapped_column(nullable=False, default=False)
	scheduled_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
	notification: Mapped[bool] = mapped_column(default=True)
	hide_media: Media[bool] = mapped_column(default=False)
