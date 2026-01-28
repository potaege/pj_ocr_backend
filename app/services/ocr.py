from typing import List, Dict, Callable, Awaitable
from fastapi import UploadFile

from app.ocr.document.thai_id import process_thai_id_image

DOC_HANDLERS: Dict[str, Callable[[List[UploadFile]], Awaitable[dict]]] = {
    "thai_id": process_thai_id_image,
}

async def process_document(doc_type: str, images: List[UploadFile]) -> dict:

    
    doc_type = doc_type.lower().strip()

    handler = DOC_HANDLERS.get(doc_type)
    if not handler:
        raise ValueError(f"Unsupported doc_type: {doc_type}")

    data = await handler(images)
    print("DEBUG type(data):", type(data))

    return data
    
    
    
