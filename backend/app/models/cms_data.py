from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class CMSData(Base):
    __tablename__ = "cms_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    crew_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    crew_name: Mapped[str] = mapped_column(String(100), nullable=False)
    crew_designation: Mapped[str] = mapped_column(String(50), nullable=False)

    fortnight_hours: Mapped[str] = mapped_column(String(20), nullable=False)

    avail_time: Mapped[str] = mapped_column(String(30), nullable=False)
    avail_station: Mapped[str] = mapped_column(String(50), nullable=False)

    status: Mapped[str] = mapped_column(String(30), nullable=False)

    called_time: Mapped[str] = mapped_column(String(30), nullable=False)
    ack_time: Mapped[str] = mapped_column(String(30), nullable=False)
    sign_on_time: Mapped[str] = mapped_column(String(30), nullable=False)
    last_signoff_time: Mapped[str] = mapped_column(String(30), nullable=False)

    train_no: Mapped[str] = mapped_column(String(20), nullable=False)
    from_station: Mapped[str] = mapped_column(String(20), nullable=False)
    to_station: Mapped[str] = mapped_column(String(20), nullable=False)

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    is_imported: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
