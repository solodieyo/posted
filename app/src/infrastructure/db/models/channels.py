from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.src.infrastructure.db.models import Base, Int64, Int16


class Channel(Base):
	__tablename__ = 'channels'
	id: Mapped[Int64] = mapped_column(primary_key=True)
	channel_id: Mapped[Int64] = mapped_column(nullable=False)
	owner_channel_id: Mapped[Int16] = mapped_column(ForeignKey('users.id'), nullable=False)
	channel_name: Mapped[str] = mapped_column(nullable=False)