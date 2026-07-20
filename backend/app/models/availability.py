from sqlalchemy import String, Integer, DateTime, Enum, ForeignKey, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date

from app.db.database import Base
from app.core.enums import AvailabilityStatus


class Availability(Base):
    __tablename__ = "availabilities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    crew_id: Mapped[int] = mapped_column(Integer, ForeignKey("crew.id"), nullable=False)
    available_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    status: Mapped[AvailabilityStatus] = mapped_column(
        Enum(
            AvailabilityStatus,
            values_callable=lambda enum: [e.value for e in enum],
            native_enum=False,
        ),
        nullable=False,
    )
    reason: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    crew: Mapped["Crew"] = relationship("Crew", back_populates="availabilities")
