from pydantic import BaseModel, Field
from datetime import date

class DrivingLicenceData(BaseModel):
    driving_licence_type: str

    driving_licence_id: str = Field(min_length=8, max_length=8)

    prefix_name_th: str
    first_name_th: str
    surname_th: str

    prefix_name_eng: str
    first_name_en: str
    surname_en: str

    birthday: date

    citizen_id: str = Field(min_length=13, max_length=13)

    issue_date: date
    expiry_date: date

    provinces_th: str
