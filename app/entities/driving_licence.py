from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class DrivingLicence(Base):
    __tablename__ = "driving_licence"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )

    driving_licence_type = Column(String, nullable=False)

    driving_licence_id = Column(String(8), nullable=False)

    prefix_name_th = Column(String(10), nullable=False)
    first_name_th = Column(String(50), nullable=False)
    surname_th = Column(String(50), nullable=False)

    prefix_name_eng = Column(String(10), nullable=False)
    first_name_en = Column(String(50), nullable=False)
    surname_en = Column(String(50), nullable=False)

    birthday = Column(Date, nullable=False)

    citizen_id = Column(String(13), nullable=False)

    issue_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)

    provinces_th = Column(String(50), nullable=False)

    created_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now()
    )

    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
