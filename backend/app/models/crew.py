from sqlalchemy import String, Integer, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db.database import Base
from app.core.enums import Department


class Crew(Base):
    __tablename__ = "crew"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    crew_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    department: Mapped[Department] = mapped_column(
        Enum(
            Department,
            values_callable=lambda enum: [e.value for e in enum],
            native_enum=False,
        ),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    assignments: Mapped[list["Assignment"]] = relationship(
        "Assignment", back_populates="crew", cascade="all, delete-orphan"
    )
    availabilities: Mapped[list["Availability"]] = relationship(
        "Availability", back_populates="crew", cascade="all, delete-orphan"
    )
