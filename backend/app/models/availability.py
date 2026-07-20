import sqlalchemy as sa
from sqlalchemy import String, Integer, DateTime, Enum, ForeignKey, Date, Boolean

from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date

from app.db.database import Base
from app.core.enums import AvailabilityStatus


class Availability(Base):
    __tablename__ = "availabilities"

    __table_args__ = (
        # Unique per crew per day for service-level duplicate prevention.
        sa.UniqueConstraint("crew_id", "available_date", name="uq_availabilities_crew_date"),
        # Helpful indexes for frequent queries/joins.
        sa.Index("ix_availabilities_crew_id", "crew_id"),
        sa.Index("ix_availabilities_available_date", "available_date"),
        sa.Index("ix_availabilities_status", "status"),
    )




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
