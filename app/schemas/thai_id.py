from pydantic import BaseModel, Field
from datetime import date

class ThaiIDData(BaseModel):
    citizen_id: str = Field(min_length=13, max_length=13)  
    
    prefix_name_th: str
    first_name_th: str
    last_name_th: str

    prefix_name_eng: str
    first_name_en: str
    last_name_en: str

    birthday: date
    religion: str

    address_rest: str
    sub_district_th: str
    district_th: str
    province_th: str

    issue_date: date
    expiry_date: date
