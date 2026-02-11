from pydantic import BaseModel
from datetime import date
from typing import Optional

class HouseRegistrationDate(BaseModel):
    house_no: str
    registry_office: str

    address_rest: str
    sub_district_th: str
    district_th: str
    province_th: str

    village_name: str
    house_name: str

    house_type: str
    house_specification: str

    date_of_registration: date
    date_of_print_house_registration: date
