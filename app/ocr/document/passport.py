import cv2
import json
import numpy as np
from app.ocr.model_ocr import run_ocr
from app.ocr.utils import collect_texts, unique_keep_order, to_debug_string
from app.ocr.re_image.preprocess import resize_image
from app.ocr.re_image.crop_regions import crop_regions
from app.ocr.filter_world.check_documents.check_passport import receive_passport_ocr_data

from typing import List, Dict, Any
from fastapi import UploadFile

REGIONS = {
    "passport_no":   (815, 100, 180, 30, True),
    "country_code":  (550, 100, 100, 30, True),
    "type":          (415, 100, 60, 30, True),
    "last_name_en":  (415, 155, 345, 25, True),
    "first_name_en": (415, 205, 345, 27, True),
    "full_name_th":  (415, 257, 435, 36, True),
    "nationality":   (415, 318, 140, 26, True),
    "date_of_birth": (595, 317, 190, 24, True),
    "identification_no": (815, 317, 220, 26, True),
    "sex":           (415, 367, 110, 28, True),
    "height":        (415, 422, 110, 28, True),
    "place_of_birth":(595, 368, 400, 26, True),
    "issue_date":    (415, 470, 180, 28, True),
    "expiry_date":   (415, 525, 180, 28, True),
}

async def process_passport_image(image: UploadFile):
   
    image_bytes = await image.read()
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("Invalid image file or decode failed")

    img = resize_image(img, 1280, 800)

    crops = crop_regions(img, REGIONS, pad_x=35,pad_y=80,save_dir="debug_crops")

    results = {}

    # 3) OCR ทีละช่อง
    for field, crop in crops.items():
        if crop is None:
            results[field] = ""
            continue

        is_addr = (field == "full_name_th")
        res, used_api = run_ocr(crop , no_doc=is_addr, no_textline=is_addr)

       

        texts = []
        collect_texts(res, texts)
        texts = [t for t in texts if len(t.strip()) >= 1]
        texts = unique_keep_order(texts)

        results[field] = " ".join(texts).strip()

    results_filter = receive_passport_ocr_data(results)
    output = format_after_filter(results_filter)
    
    return output
    


def  format_after_filter(data):

    result = {
        "type": data["type"],
        "country_code": data["country_code"],
        "passport_no": data["passport_no"], 

        "prefix_name_th": data["prefix_name_th"], 
        "first_name_th": data["name_th"],
        "surname_th": data["last_name_th"],

        "prefix_name_eng ": data["prefix_name_en"], 
        "first_name_eng ": data["first_name_en"],
        "surname_eng": data["last_name_en"], 

        "nationality": data["nationality"],
        "citizen_id": data["identification_no"], 
        "birthday": data["date_of_birth"], 

        "sex": data["sex"], 
        "height": data["height"],
        "place_of_birth": data["place_of_birth"],

        "issue_date": data["issue_date"],
        "expiry_date": data["expiry_date"]

    }

    return result
   