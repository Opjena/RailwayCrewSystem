from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from app.core.enums import Department


class Crew(Base):
    __tablename__ = "crew"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    crew_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    department: Mapped[Department] = mapped_column(
        Enum(
            Department,
            values_callable=lambda enum: [e.value for e in enum],
            native_enum=False,
        ),
        nullable=False,
    )

    mobile_number: Mapped[str] = mapped_column(
        String(15),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    designation: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )