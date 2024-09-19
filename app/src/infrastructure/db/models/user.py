from sqlalchemy.orm import Mapped, mapped_column

from app.src.infrastructure.db.models import Base, Int64, Int16


class User(Base):
	__tablename__ = 'users'

	id: Mapped[Int16] = mapped_column(primary_key=True)
	tg_user_id: Mapped[Int64]
	username: Mapped[str]
	full_name: Mapped[str]

