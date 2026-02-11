from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class Passport(Base):
    __tablename__ = "passport"

    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True
    )

    country_code = Column(String(3), nullable=False)
    passport_no = Column(String(9), nullable=False)

    prefix_name_eng = Column(String(10), nullable=False)
    first_name_eng = Column(String(50), nullable=False)
    surname_eng = Column(String(50), nullable=False)

    prefix_name_th = Column(String(10), nullable=False)
    first_name_th = Column(String(50), nullable=False)
    surname_th = Column(String(50), nullable=False)

    nationality = Column(String(50), nullable=False)

    citizen_id = Column(String(13), nullable=False)

    birthday = Column(Date, nullable=False)

    sex = Column(String(1), nullable=False)

    height = Column(Integer, nullable=False)

    place_of_birth = Column(String(50), nullable=False)

    issue_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)

    type = Column(String(1), nullable=False)

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
