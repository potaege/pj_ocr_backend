import cv2
import json
import numpy as np
from app.ocr.model_ocr import run_ocr
from app.ocr.utils import collect_texts, unique_keep_order, to_debug_string
from app.ocr.re_image.preprocess import resize_image
from app.ocr.re_image.crop_regions import crop_regions
from app.ocr.filter_world.check_documents.check_house_registration import receive_house_registration_ocr_data

from typing import List, Dict, Any
from fastapi import UploadFile

REGIONS = {
    "house_no":   (255, 110, 315, 70, False),
    "registry_office":  (785, 110, 390, 70, False),
    "address":          (165, 180, 870, 130, True), # address มีแล้ว
    "village_name":  (165, 330, 420, 70, False),
    "house_name": (710, 330, 450, 70, True),
    "house_type":  (165, 400, 420, 70, False),
    "house_specification":   (765, 400, 450, 70, False),
    "date_of_registration": (350, 480, 350, 60, False),
    "date_of_print_house_registration": (950, 660, 270, 50, False),
}

async def process_house_registration_image(image: UploadFile):

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

        is_addr = (field == "address") 
        res, used_api = run_ocr(crop , no_doc=is_addr, no_textline=is_addr)

        texts = []
        collect_texts(res, texts)
        texts = [t for t in texts if len(t.strip()) >= 1]
        texts = unique_keep_order(texts)

        results[field] = " ".join(texts).strip()

   
    results_filter = receive_house_registration_ocr_data(results)
    output = format_after_filter(results_filter)
    
    return output

    
def  format_after_filter(data):

    result = {
        "house_no": data["house_no"],
        "registry_office": data["registry_office"],

        "address_rest": data["address_rest"], 
        "sub_district_th": data["sub_district_th"], 
        "district_th": data["district_th"],
        "province_th": data["province_th"],

        "village_name": data["village_name"], 

        "house_name": data["house_name"],
        "house_type": data["house_type"], 
        "house_specification": data["house_specification"],

        "date_of_registration": data["date_of_registration"], 
        "date_of_print_house_registration": data["date_of_print_house_registration"], 
    }

    return result
