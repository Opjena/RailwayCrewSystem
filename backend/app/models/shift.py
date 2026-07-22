from datetime import datetime, date, time

from sqlalchemy import String, Integer, DateTime, Time, Enum, ForeignKey, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.core.enums import ShiftType


class Shift(Base):
    __tablename__ = "shifts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    shift_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    shift_type: Mapped[ShiftType] = mapped_column(
        Enum(
            ShiftType,
            values_callable=lambda enum: [e.value for e in enum],
            native_enum=False,
        ),
        nullable=False,
    )
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    crew_required: Mapped[int] = mapped_column(Integer, default=1)
    location: Mapped[str] = mapped_column(String(100), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    assignments = relationship("Assignment", back_populates="shift")
