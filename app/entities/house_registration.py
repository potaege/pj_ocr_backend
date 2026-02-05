from sqlalchemy import Column, Integer, String, Date, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class HouseRegistration(Base):
    __tablename__ = "house_registration"

    id = Column(Integer, primary_key=True)

    house_no = Column(String(20), nullable=False)
    registry_office = Column(String(100), nullable=False)

    address_rest = Column(Text, nullable=False)
    sub_district_th = Column(String(50), nullable=False)
    district_th = Column(String(50), nullable=False)
    province_th = Column(String(50), nullable=False)

    village_name = Column(String(50), nullable=False)
    house_name = Column(String(50), nullable=False)

    house_type = Column(String(25), nullable=False)
    house_specification = Column(Text, nullable=False)

    date_of_registration = Column(Date, nullable=False)
    date_of_print_house_registration = Column(Date, nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False
    )

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
