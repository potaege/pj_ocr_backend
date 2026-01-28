from pydantic import BaseModel, Field ,ConfigDict
from typing import Union, Literal

from app.schemas.thai_id import ThaiIDData
# from app.schemas.passport import PassportData
# from app.schemas.driver_license import DriverLicenseData

class ThaiIDCreate(BaseModel):
    doc_type: Literal["thai_id"]
    data: ThaiIDData
    model_config = ConfigDict(extra="allow")

# class PassportCreate(BaseModel):
#     doc_type: Literal["passport"]
#     user_id: int
#     data: PassportData

# class DriverLicenseCreate(BaseModel):
#     doc_type: Literal["driver_license"]
#     user_id: int
#     data: DriverLicenseData


DocumentCreate = Union[ThaiIDCreate]
# DocumentCreate = Union[ThaiIDCreate, PassportCreate, DriverLicenseCreate]