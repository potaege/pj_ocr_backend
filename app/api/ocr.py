from fastapi import APIRouter , UploadFile, File ,Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from app.db.deps import get_db
from fastapi import HTTPException

import app.services.ocr as service_ocr

router = APIRouter(prefix="/ocr", tags=["ocr"])

@router.get("/")
def root():
    return {"message": "ocr is ok"}

@router.post("/process/{doc_type}")
async def ocr_parts(doc_type: str ,
                    images: List[UploadFile] = File(...),
                    ):

    try :
        
        data = await service_ocr.process_document(doc_type,images)

        return {
            "status" : True,
            "data" : data
        }

    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))