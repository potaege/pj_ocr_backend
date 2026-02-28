from app.schemas.document import ThaiIDCreate ,PassportCreate ,HouseRegistrationCreate,DriverLicenseCreate

from app.services.thai_id import add_thai_id
from app.models.passport import add_passport
from app.models.house_registration import add_house_registration
from app.models.driving_licence import add_driving_licence

from pydantic import ValidationError

import app.models.thai_id as model_thai_id
import app.models.driving_licence as model_driving_licence
import app.models.passport as model_passport
import app.models.house_registration as model_house_registration

from app.views.formatter import format

from app.helper.help_format_thai_id import format_thai_id
from app.helper.help_format_driving_licence import format_driving_licence
from app.helper.help_format_passport import format_passport
from app.helper.help_format_house_registration import format_house_registration

SCHEMA_MAP = {
    "thai_id": ThaiIDCreate,
    "passport" : PassportCreate,
    "house_registration" : HouseRegistrationCreate,
    "driving_licence" : DriverLicenseCreate

}

DOCUMENT_HANDLER = {
    "thai_id": add_thai_id,
    "passport": add_passport,
    "house_registration" : add_house_registration,
    "driving_licence" : add_driving_licence
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
    id = data["id"]

    match doc_type:

        case "thai_id":
            data = model_thai_id.edit_thai_id(db,user_id ,data_in)

        case "driving_licence":
            data = model_driving_licence.edit_driving_licence(db,id,data_in)

        case "passport":
            data = model_passport.edit_passport(db,user_id ,data_in)

        case "house_registration":
             data= model_house_registration.edit_house_registration(db,id,data_in)

        case _:
            return None
    return True

def get_document_by_id(db, doc_type,id):

    match doc_type:

        case "driving_licence":
            data = model_driving_licence.get_driving_licence_by_id(db,id)

        case "house_registration":
             data= model_house_registration.get_house_registration_by_id(db,id)

        case _:
            return None
    return data



def _clean(v):
    return v.strip() if isinstance(v, str) else v

def _get(doc, key):
    # doc เป็น dict
    return _clean(doc.get(key))

def to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

def check_document_mismatch(db, user_id: int):

    data_thai = model_thai_id.get_thai_id_by_user(db, user_id)
    data_driving_licence = model_driving_licence.get_driving_licence_by_user(db, user_id)
    data_passport = model_passport.get_passport_by_user(db, user_id)

    blocks = {}
    if data_thai:
        blocks["thai_id"] = to_dict(data_thai)

    if data_passport:
        blocks["passport"] = to_dict(data_passport)

    if data_driving_licence:
        for val in data_driving_licence:
            name = "driving_licence_" + str(val.driving_licence_type)
            blocks[name] = to_dict(val)

    if len(blocks) <= 1:
        return {}

    FIELD_MAP = {
        "citizen_id": {
            "thai_id": "citizen_id",
            "driving_licence": "citizen_id",
            "passport": "citizen_id",
        },
        "prefix_name_th": {
            "thai_id": "prefix_name_th",
            "driving_licence": "prefix_name_th",
            "passport": "prefix_name_th",
        },
        "first_name_th": {
            "thai_id": "first_name_th",
            "driving_licence": "first_name_th",
            "passport": "first_name_th",
        },

        "surname_th": {
            "thai_id": "last_name_th",
            "driving_licence": "surname_th",
            "passport": "surname_th",
        },

        "prefix_name_eng": {
            "thai_id": "prefix_name_eng",
            "driving_licence": "prefix_name_eng",
            "passport": "prefix_name_eng",
        },

        "first_name_eng": {
            "thai_id": "first_name_en",
            "driving_licence": "first_name_en",
            "passport": "first_name_eng",
        },

    
        "surname_eng": {
            "thai_id": "last_name_en",
            "driving_licence": "surname_en",
            "passport": "surname_eng",
        },

        "birthday": {
            "thai_id": "birthday",
            "driving_licence": "birthday",
            "passport": "birthday",
        },
    }

    mismatches = {}

    for field_name, mapping in FIELD_MAP.items():
        values = {}

        for block_key, doc in blocks.items():
    
            doc_type = "driving_licence" if block_key.startswith("driving_licence_") else block_key

            doc_field = mapping.get(doc_type)
            if not doc_field:
                continue

            values[block_key] = _get(doc, doc_field)

        non_empty = [v for v in values.values() if v not in (None, "")]
        if len(non_empty) <= 1:
            continue

        if len(set(non_empty)) > 1:
            mismatches[field_name] = values

    if not mismatches:
        return mismatches

    return mismatches

def edit_check_document(db,field, value,user_id):

    data={}

    FIELD_MAP = {
        "citizen_id": {
            "thai_id": "citizen_id",
            "driving_licence": "citizen_id",
            "passport": "citizen_id",
        },
        "prefix_name_th": {
            "thai_id": "prefix_name_th",
            "driving_licence": "prefix_name_th",
            "passport": "prefix_name_th",
        },
        "first_name_th": {
            "thai_id": "first_name_th",
            "driving_licence": "first_name_th",
            "passport": "first_name_th",
        },

        "surname_th": {
            "thai_id": "last_name_th",
            "driving_licence": "surname_th",
            "passport": "surname_th",
        },

        "prefix_name_eng": {
            "thai_id": "prefix_name_eng",
            "driving_licence": "prefix_name_eng",
            "passport": "prefix_name_eng",
        },

        "first_name_eng": {
            "thai_id": "first_name_en",
            "driving_licence": "first_name_en",
            "passport": "first_name_eng",
        },

    
        "surname_eng": {
            "thai_id": "last_name_en",
            "driving_licence": "surname_en",
            "passport": "surname_eng",
        },

        "birthday": {
            "thai_id": "birthday",
            "driving_licence": "birthday",
            "passport": "birthday",
        },
    }

    data_thai = model_thai_id.get_thai_id_by_user(db, user_id)
    data_driving_licence = model_driving_licence.get_driving_licence_by_user(db, user_id)
    data_passport = model_passport.get_passport_by_user(db, user_id)


    data_thai_in = {}
    data_passport_in = {}
    data_driving_licence_in = {}

    if data_thai:
        data_thai_in[FIELD_MAP[field]["thai_id"]] = value
        data = model_thai_id.edit_thai_id(db,user_id ,data_thai_in)
       

    if data_passport:
        data_passport_in[FIELD_MAP[field]["passport"]] = value
        data = model_passport.edit_passport(db,user_id ,data_passport_in)
        
           
    if data_driving_licence:

        data_driving_licence_in[FIELD_MAP[field]["driving_licence"]] = value
        for val in data_driving_licence:
            id = val.id
            data_e = model_driving_licence.edit_driving_licence(db,id,data_driving_licence_in)

    return data_e

def get_all_document_format(db,user_id : int):

    data = {}

    data_thai = model_thai_id.get_thai_id_by_user(db,user_id)
    data_driving_licence = model_driving_licence.get_driving_licence_by_user(db,user_id)
    data_passport = model_passport.get_passport_by_user(db,user_id)
    data_house_registration= model_house_registration.get_house_registration_by_user(db,user_id)

    data["data_thai"] = format_thai_id(data_thai)
    data["data_driving_licence"] = format_driving_licence(data_driving_licence)
    data["data_passport"] = format_passport(data_passport)
    data["data_house_registration"] = format_house_registration(data_house_registration)
 
    return data