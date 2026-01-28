import cv2
import json
import numpy as np
from app.ocr.model_ocr import run_ocr
from app.ocr.utils import collect_texts, unique_keep_order, to_debug_string
from app.ocr.filter_world.check_documents.check_thai_id import receive_thai_id_ocr_data

from typing import List, Dict, Any
from fastapi import UploadFile

REQUIRED_FIELDS = {
    "citizen_id",
    "name_lastname_th",
    "name_eng",
    "lastname_eng",
    "birthday",
    "religion",
    "address",
    "issue_date",
    "expiry_date"
}

async def process_thai_id_image(images: List[UploadFile]) :
    
    if not images:
        raise ValueError("No images uploaded")

    image_map: Dict[str, UploadFile] = {}
    results = {}


    for f in images:
        # ดึง field จากชื่อไฟล์
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

        is_addr = (field == "address") 
        res, used_api = run_ocr(img , no_doc=is_addr, no_textline=is_addr)

        texts = []
        collect_texts(res, texts)
        texts = [t for t in texts if len(t.strip()) >= 1]
        texts = unique_keep_order(texts)

        results[field] = " ".join(texts).strip()

    

    results_filter = receive_thai_id_ocr_data(results)

    
    return results_filter
    


