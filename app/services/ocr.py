from typing import List, Dict, Callable, Awaitable
from fastapi import UploadFile

from app.ocr.document.thai_id import process_thai_id_image
from app.ocr.document.driving_license import process_driving_license
from app.ocr.document.passport import process_passport_image
from app.ocr.document.house_registration import process_house_registration_image


DOC_HANDLERS: Dict[str, Callable[[UploadFile], Awaitable[dict]]] = {
    "thai_id": process_thai_id_image,
    "driving_licence" : process_driving_license,
    "passport" : process_passport_image,
    "house_registration" : process_house_registration_image,

}

async def process_document(doc_type: str,image: UploadFile) -> dict:

    
    doc_type = doc_type.lower().strip()

    handler = DOC_HANDLERS.get(doc_type)
    if not handler:
        raise ValueError(f"Unsupported doc_type: {doc_type}")

    data = await handler(image)

    return data
    
    
    
