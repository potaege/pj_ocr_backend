import cv2
import json
from app.ocr.model_ocr import run_ocr
from app.ocr.utils import collect_texts, unique_keep_order, to_debug_string
from app.ocr.filter_world.check_documents.check_passport import receive_passport_ocr_data

import numpy as np
from typing import List, Dict, Any
from fastapi import UploadFile

REQUIRED_FIELDS = {
    "passport_no",
    "country_code",
    "type",
    "last_name_en",
    "first_name_en",
    "full_name_th",
    "nationality",
    "date_of_birth",
    "identification_no",
    "sex",
    "height",
    "place_of_birth",
    "issue_date",
    "expiry_date",
}

async def process_passport_image(images: List[UploadFile]):
    
    if not images:
        raise ValueError("No images uploaded")

    image_map: Dict[str, UploadFile] = {}

    for f in images:
        field = f.filename.split(".")[0].lower()
        image_map[field] = f

    missing = REQUIRED_FIELDS - image_map.keys()
    if missing:
        raise ValueError(f"No images  {', '.join(missing)}")

    results: Dict[str, str] = {}

    for field in REQUIRED_FIELDS:
        
        file = image_map[field]
        image_bytes = await file.read()
        img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

        is_addr = (field == "full_name_th")
        res, used_api = run_ocr(img , no_doc=is_addr, no_textline=is_addr)


        texts = []
        collect_texts(res, texts)
        texts = [t for t in texts if len(t.strip()) >= 1]
        texts = unique_keep_order(texts)

        results[field] = " ".join(texts).strip()


    results_filter = receive_passport_ocr_data(results)

    return results_filter
   
