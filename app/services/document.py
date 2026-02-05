from app.schemas.document import ThaiIDCreate

from app.services.thai_id import add_thai_id

from pydantic import ValidationError

import app.models.thai_id as model_thai_id
import app.models.driving_licence as model_driving_licence
import app.models.passport as model_passport
import app.models.house_registration as model_house_registration

from app.views.formatter import format


SCHEMA_MAP = {
    "thai_id": ThaiIDCreate,

}

DOCUMENT_HANDLER = {
    "thai_id": add_thai_id
}

def add_document(db, user_id: int, data):

    doc_type = data["doc_type"]

    schema_cls = SCHEMA_MAP.get(doc_type)
    handler = DOCUMENT_HANDLER.get(doc_type)

    if not schema_cls or not handler:
        raise ValueError("Unknown document type")

    try:
        schema_cls.model_validate(data)
        
        data_in = data["data"]
        data_in["user_id"] = user_id

        add_doc = handler(db, data_in)

        return add_doc
   
    except ValidationError as e:
        raise ValueError(e.errors())
    
def get_all_document(db,user_id : int):

    data = {}

    data_thai = model_thai_id.get_thai_id_by_user(db,user_id)
    data_driving_licence = model_driving_licence.get_driving_licence_by_user(db,user_id)
    data_passport = model_passport.get_passport_by_user(db,user_id)
    data_house_registration= model_house_registration.get_house_registration_by_user(db,user_id)

    # data_thai = format(data_thai,"thai_id","full")

    data["data_thai"] = data_thai 
    data["data_driving_licence"] = data_driving_licence
    data["data_passport"] = data_passport
    data["data_house_registration"] = data_house_registration

    return data


def get_document_by_user(db, doc_type,user_id):

    match doc_type:

        case "thai_id":
            data = model_thai_id.get_thai_id_by_user(db,user_id)

        case "driving_licence":
            data = model_driving_licence.get_driving_licence_by_user(db,user_id)

        case "passport":
            data = model_passport.get_passport_by_user(db,user_id)

        case "house_registration":
             data= model_house_registration.get_house_registration_by_user(db,user_id)

        case _:
            return None
    return data


def edit_document(db,user_id,data):

    doc_type = data["doc_type"]

    data_in = data["data"]
    match doc_type:

        case "thai_id":
            data = model_thai_id.edit_thai_id(db,user_id ,data_in)

        # case "driving_licence":
        #     data = model_driving_licence.get_driving_licence_by_user(db,user_id)

        # case "passport":
        #     data = model_passport.get_passport_by_user(db,user_id)

        # case "house_registration":
        #      data= model_house_registration.get_house_registration_by_user(db,user_id)

        case _:
            return None
    return True
 
