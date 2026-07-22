from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class CMSData(Base):
    __tablename__ = "cms_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    crew_id: Mapped[str] = mapped_column(String(20), index=True)
    crew_name: Mapped[str] = mapped_column(String(100))
    crew_designation: Mapped[str] = mapped_column(String(50))

    fortnight_hours: Mapped[str] = mapped_column(String(20))

    avail_time: Mapped[str] = mapped_column(String(30))
    avail_station: Mapped[str] = mapped_column(String(50))

    status: Mapped[str] = mapped_column(String(30))

    called_time: Mapped[str] = mapped_column(String(30))
    ack_time: Mapped[str] = mapped_column(String(30))
    sign_on_time: Mapped[str] = mapped_column(String(30))
    last_signoff_time: Mapped[str] = mapped_column(String(30))

    train_no: Mapped[str] = mapped_column(String(20))
    from_station: Mapped[str] = mapped_column(String(20))
    to_station: Mapped[str] = mapped_column(String(20))

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

