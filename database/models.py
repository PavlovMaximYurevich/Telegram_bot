from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Event(Base):
    __tablename__ = 'event'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    event_name: Mapped[str] = mapped_column(nullable=False)
    event_link: Mapped[str] = mapped_column(Text, nullable=False)
    contact_tg: Mapped[str] = mapped_column(nullable=False)

