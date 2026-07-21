from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class MainData(Base):
    __tablename__ = "main_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    signon_id: Mapped[int] = mapped_column(ForeignKey("signon_data.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )