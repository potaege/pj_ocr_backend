from pydantic import BaseModel, Field ,ConfigDict
from typing import Union, Literal

from app.schemas.thai_id import ThaiIDData
from app.schemas.passport import PassportData
from app.schemas.house_registration import HouseRegistrationDate
from app.schemas.driving_licence import DrivingLicenceData

class ThaiIDCreate(BaseModel):
    doc_type: Literal["thai_id"]
    data: ThaiIDData
    model_config = ConfigDict(extra="allow")

class PassportCreate(BaseModel):
    doc_type: Literal["passport"]
    data: PassportData
    model_config = ConfigDict(extra="allow")

class HouseRegistrationCreate(BaseModel):
    doc_type: Literal["house_registration"]
    data: HouseRegistrationDate
    model_config = ConfigDict(extra="allow")

class DriverLicenseCreate(BaseModel):
    doc_type: Literal["driving_licence"]
    data: DrivingLicenceData
    model_config = ConfigDict(extra="allow")


DocumentCreate = Union[ThaiIDCreate,PassportCreate,HouseRegistrationCreate ,DriverLicenseCreate ]