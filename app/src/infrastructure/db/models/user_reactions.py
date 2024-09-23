from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.src.infrastructure.db.models import Base, Int16


class UserReaction(Base):
	__tablename__ = 'user_reactions'

	id: Mapped[Int16] = mapped_column(primary_key=True, autoincrement=True)
	user_id: Mapped[Int16] = mapped_column(ForeignKey('users.id'), nullable=False)
	reaction_id: Mapped[Int16] = mapped_column(ForeignKey('reactions.id'), nullable=False)
	post_id: Mapped[Int16] = mapped_column(ForeignKey('posts.id'), nullable=False)