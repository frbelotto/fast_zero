from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass()
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), init=False)
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now()   
    )

    # Parei em https://www.youtube.com/live/I7IrmN7jMqE?si=_jYrejvGMkvMWQdE&t=1524
