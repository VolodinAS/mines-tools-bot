from datetime import datetime, timezone as tz

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class CrystalPrice(Base):
    __tablename__ = "crystal_prices"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(tz.utc)
    )
    green: Mapped[int] = mapped_column(Integer)
    blue: Mapped[int] = mapped_column(Integer)
    red: Mapped[int] = mapped_column(Integer)
    violet: Mapped[int] = mapped_column(Integer)
    white: Mapped[int] = mapped_column(Integer)
    cyan: Mapped[int] = mapped_column(Integer)
