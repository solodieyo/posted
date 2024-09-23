from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.src.infrastructure.db.models import Base, Int16, Int64


class Reaction(Base):
	__tablename__ = 'reactions'

	id: Mapped[Int16] = mapped_column(primary_key=True, autoincrement=True)
	emoji: Mapped[str] = mapped_column(nullable=False)
	message_id: Mapped[Int64] = mapped_column(nullable=True)
	channel_id: Mapped[Int16] = mapped_column(nullable=False)
	post_id: Mapped[Int16] = mapped_column(ForeignKey('posts.id'), nullable=False)
	count_reaction: Mapped[int] = mapped_column(default=0)