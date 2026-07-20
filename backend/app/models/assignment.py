from sqlalchemy import String, Integer, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db.database import Base
from app.core.enums import AssignmentStatus


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    shift_id: Mapped[int] = mapped_column(Integer, ForeignKey("shifts.id"), nullable=False)
    crew_id: Mapped[int] = mapped_column(Integer, ForeignKey("crew.id"), nullable=False)
    status: Mapped[AssignmentStatus] = mapped_column(
        Enum(
            AssignmentStatus,
            values_callable=lambda enum: [e.value for e in enum],
            native_enum=False,
        ),
        default=AssignmentStatus.ASSIGNED,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    shift: Mapped["Shift"] = relationship("Shift", back_populates="assignments")
    crew: Mapped["Crew"] = relationship("Crew", back_populates="assignments")
