import cv2
import json
import numpy as np
from app.ocr.model_ocr import run_ocr
from app.ocr.utils import collect_texts, unique_keep_order, to_debug_string
from app.ocr.re_image.preprocess import resize_image
from app.ocr.re_image.crop_regions import crop_regions 
from app.ocr.filter_world.check_documents.check_driving_license import receive_driving_license_data

from typing import List, Dict, Any
from fastapi import UploadFile

from app.ocr.re_image.preprocess import resize_image
from app.ocr.re_image.crop_regions import crop_regions 

REGIONS = {
    "car_type": (575, 77, 588, 49, True),          
    "car_id1": (467, 150, 273, 55, True),
    "car_id2": (839, 153, 320, 53, True),
    "issue_date_thai": (499, 210, 262, 45, True),
    "issue_date_eng": (515, 253, 192, 37, True),
    "expiry_date_thai": (929, 215, 262, 43, True),
    "expiry_date_eng": (945, 255, 196, 39, True),
    "name_lastname_th": (410, 339, 839, 83, True),
    "name_lastName_eng": (447, 422, 805, 100, True),
    "birth_date_th": (492, 523, 296, 60, True), ##
    "birth_date_eng": (502, 580, 256, 57, True),
    "thai_id": (760, 623, 393, 55, True),
    "registrar": (487, 698, 765, 68, True),
}

async def process_driving_license(image: UploadFile):

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

        res, used_api = run_ocr(crop , False, False)

       
        texts = []
        collect_texts(res, texts)
        texts = [t for t in texts if len(t.strip()) >= 1]
        texts = unique_keep_order(texts)

        results[field] = " ".join(texts).strip()



    results_filter = receive_driving_license_data(results)
    output = format_after_filter(results_filter)

    return output
    



def  format_after_filter(data):

    result = {
        # "driving_licence_type": data["car_type"],##
        "driving_licence_id": data["car_id_2"],##

        "issue_date": data["issue_date_eng"], ##
        "expiry_date": data["expiry_date_eng"], ##

        "prefix_name_th": data["prefix_name_th"],##
        "first_name_th": data["name_th"],##
        "surname_th": data["last_name_th"], ## 

        "prefix_name_eng": data["prefix_name_eng"],##
        "first_name_en": data["name_eng"], ## 
        "surname_en": data["last_name_eng"],##

        "birthday": data["birth_date_eng"], ##

        "citizen_id": data["thai_id"], ##

        "provinces_th": data["provinces_th"], ##
        "provinces_eng": data["provinces_eng"],
        "registrar_index": data["nums_list"][0],

    }

    return result
