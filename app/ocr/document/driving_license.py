import cv2
import json
from app.ocr.model_ocr import run_ocr
from app.ocr.utils import collect_texts, unique_keep_order, to_debug_string
from app.ocr.filter_world.check_documents.check_driving_license import receive_driving_license_data

import numpy as np
from typing import List, Dict, Any
from fastapi import UploadFile

REQUIRED_FIELDS = {
    "car_type",          
    "car_id1",
    "car_id2",
    "issue_date_thai",
    "issue_date_eng",
    "expiry_date_thai",
    "expiry_date_eng",
    "name_lastname_th",
    "name_lastName_eng",
    "birth_date_th", 
    "birth_date_eng",
    "thai_id",
    "registrar",
}


async def process_driving_license(images: List[UploadFile]):

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

        res, used_api = run_ocr(img , False, False)


        texts = []
        collect_texts(res, texts)
        texts = [t for t in texts if len(t.strip()) >= 1]
        texts = unique_keep_order(texts)

        results[field] = " ".join(texts).strip()


    results_filter = receive_driving_license_data(results)
    results_filter = format_after_filter(results_filter)
    
    return results_filter



def  format_after_filter(data):

    result = {
        "driving_licence_type": data["car_type"],##
        "driving_licence_id": data["car_id_2"],##

        "issue_date": data["issue_date_eng"], ##
        "expiry_date": data["expiry_date_eng"], ##

        "prefix_name_th": data["prefix_name_th"],##
        "name_th": data["name_th"],##
        "last_name_th": data["last_name_th"], ## 

        "prefix_name_eng": data["prefix_name_eng"],##
        "name_eng": data["name_eng"], ## 
        "last_name_eng": data["last_name_eng"],##

        "birth_date": data["birth_date_eng"], ##

        "citizen_id": data["thai_id"], ##

        "provinces_th": data["provinces_th"], ##
        "provinces_eng": data["provinces_eng"],

        "registrar_index": data["nums_list"][0],

    }

    return result

