from app.schemas.document import ThaiIDCreate

from app.services.thai_id import add_thai_id

from pydantic import ValidationError



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
    


 
