from pydantic import BaseModel, Field
from datetime import date
from enum import Enum
from typing import Optional


class SexEnum(str, Enum):
    M = "M"
    F = "F"
    X = "X"


class PassportData(BaseModel):

    type: str 

    country_code: str = Field(min_length=3,max_length=3,)

    passport_no: str

    prefix_name_th: str
    first_name_th: str
    surname_th: str

    prefix_name_eng: str
    first_name_eng: str
    surname_eng: str

    nationality: str

    citizen_id: str 

    birthday: date

    sex: SexEnum
    height: str

    place_of_birth: str

    issue_date: date
    expiry_date: date
