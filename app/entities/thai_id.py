from sqlalchemy import Column, Integer, String, Date, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class ThaiID(Base):
    __tablename__ = "thai_id"

    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True
    )

    citizen_id = Column(String(13), nullable=False, unique=True)

    prefix_name_th = Column(String(10), nullable=False)
    first_name_th = Column(String(50), nullable=False)
    last_name_th = Column(String(50), nullable=False)

    prefix_name_eng = Column(String(10), nullable=False)
    first_name_en = Column(String(50), nullable=False)
    last_name_en = Column(String(50), nullable=False)

    birthday = Column(Date, nullable=False)
    religion = Column(String(50), nullable=False)

    address_rest = Column(Text, nullable=False)
    sub_district_th = Column(Text, nullable=False)
    district_th = Column(Text, nullable=False)
    province_th = Column(Text, nullable=False)

    issue_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)

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
