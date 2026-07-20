from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.db.database import Base


class Duty(Base):
    __tablename__ = "duties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # PRD-aligned fields are TODO until PRD table spec is fully known.
    duty_code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

