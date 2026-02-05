import cv2
import json
import numpy as np
from app.ocr.model_ocr import run_ocr
from app.ocr.utils import collect_texts, unique_keep_order, to_debug_string
from app.ocr.filter_world.check_documents.check_thai_id import receive_thai_id_ocr_data

from typing import List, Dict, Any
from fastapi import UploadFile

from app.ocr.re_image.preprocess import resize_image
from app.ocr.re_image.crop_regions import crop_regions 



REGIONS = {
    "citizen_id": (554, 82, 421, 54 ,False), ##พิกัดcrop 4ตัวหน้า แล้วตัวท้ายสุดคือ ต้องการให้ ภาพที่มีพื้นหลังสีอื่นทำให้กลายเป็นสีขาวไหม
    "name_lastname_th": (355 ,149, 889, 93,True),
    "name_eng": (498, 251, 558, 54,True),
    "lastname_eng": (568, 293, 519, 47,True),
    "birthday": (550, 340, 279, 66,True),
    "religion": (529, 470, 122, 47,True),
    "address": (135, 511, 763, 121,True),
    "issue_date": (137, 632, 190, 38,True),
    "expiry_date": (700, 623, 192, 45,True),
}


async def process_thai_id_image(image: UploadFile) :
    
    image_bytes = await image.read()
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("Invalid image file or decode failed")

    img = resize_image(img, 1280, 800)

    crops = crop_regions(img, REGIONS, pad_x=35,pad_y=80,save_dir="debug_crops")

    results = {}

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

    results_filter = receive_thai_id_ocr_data(results)
    output = format_after_filter(results_filter)

    return output
    

def  format_after_filter(data):

    result = {
        "citizen_id": data["citizen_id"],

        "prefix_name_th": data["prefix_name_th"],
        "first_name_th": data["name_th"], ##
        "last_name_th": data["last_name_th"], ##

        "prefix_name_eng": data["prefix_name_eng"],##
        "first_name_en": data["name_eng"],##
        "last_name_en": data["last_name_eng"], ## 

        "birthday": data["birthday"],##
        "religion": data["religion"], ## 

        "address_rest": data["address_rest"],##
        "sub_district_th": data["sub_district_th"], ##
        "district_th": data["district_th"], ##
        "province_th": data["province_th"], 

        "issue_date": data["issue_date"],
        "expiry_date": data["expiry_date"],

    }

    return result
