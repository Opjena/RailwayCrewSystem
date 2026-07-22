from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class SignOnData(Base):
    __tablename__ = "signon_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    cms_id: Mapped[int] = mapped_column(ForeignKey("cms_data.id"))

    crew_id: Mapped[str] = mapped_column(String(20))
    crew_name: Mapped[str] = mapped_column(String(100))

    status: Mapped[str] = mapped_column(String(30))

    train_no: Mapped[str] = mapped_column(String(20))
    from_station: Mapped[str] = mapped_column(String(20))
    to_station: Mapped[str] = mapped_column(String(20))

    sign_on_time: Mapped[str] = mapped_column(String(30))

    cto_train_no: Mapped[str] = mapped_column(String(20))
    cto_station: Mapped[str] = mapped_column(String(20))
    cto_time: Mapped[str] = mapped_column(String(30))

    loco1: Mapped[str] = mapped_column(String(20))
    loco2: Mapped[str] = mapped_column(String(20))
    loco3: Mapped[str] = mapped_column(String(20))

    shed: Mapped[str] = mapped_column(String(30))

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

