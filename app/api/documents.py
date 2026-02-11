from fastapi import APIRouter , Depends , Body
from pydantic import BaseModel

from sqlalchemy.orm import Session
from app.db.deps import get_db
import app.services.document as service_document
import app.services.thai_id as service_thai_id
from typing import Optional

router = APIRouter(prefix="/documents", tags=["documents"])

@router.get("/")
def root():
    return {"message": "documents is ok"}



@router.get("/getThaiID/{user_id}")
def get_thai_id(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        data = service_thai_id.get_thai_id_by_user(db, user_id)

        return {
            "status": True,
            "data": data
        }
    
    except Exception as e:
        return {
        "status": False,
        "message": str(e)
    }


@router.post("/add_document/{user_id}")
def create_document(
    data: dict,
    user_id :int,
    db: Session = Depends(get_db)):
    try:
   
        result = service_document.add_document(db,user_id, data)
       
        return {
            "success": True,
            "data": result
        }
    
    except Exception as e:
        return {
        "status": False,
        "message": str(e)
    }


@router.get("/get_all_document/{user_id}")
def get_all_document(
    user_id :int, 
    db: Session = Depends(get_db)):
    try:
   
        data = service_document.get_all_document(db,user_id)
        mismatch = service_document.check_document_mismatch(db,user_id)

        return {
            "success": True,
            "data": data,
            "mismatch" : len(mismatch)
        }
    
    except Exception as e:
        return {
        "status": False,
        "message": str(e)
    }


@router.get("/get_document/{doc_type}/{user_id}")
def get_document(
    doc_type : str,
    user_id :int,
    db: Session = Depends(get_db)):
    try:
   
        data = service_document.get_document_by_user(db,doc_type,user_id)
       

        return {
            "success": True,
            "data": data,
        }
    
    except Exception as e:
        return {
        "status": False,
        "message": str(e)
    }


@router.post("/edit_document/{user_id}")
def edit_document(
    data: dict,
    user_id :int, 
    db: Session = Depends(get_db)):
    try:
   
        result = service_document.edit_document(db,user_id, data)
    
        return {
            "success": True,
            "data": result
        }
    
    except Exception as e:
        return {
        "status": False,
        "message": str(e)
    }

@router.get("/get_document_by_id/{doc_type}/{id}")
def get_document_by_id(
    doc_type : str,
    id :int,
    db: Session = Depends(get_db)):
    try:
   
        data = service_document.get_document_by_id(db,doc_type,id)
       
        return {
            "success": True,
            "data": data,
        }
    
    except Exception as e:
        return {
        "status": False,
        "message": str(e)
    }

@router.get("/check_document_mismatch/{user_id}")
def check_document_mismatch(
    user_id :int, 
    db: Session = Depends(get_db)):
    try:
   
        mismatch = service_document.check_document_mismatch(db,user_id)

        return {
            "success": True,
            "mismatch" : mismatch
        }
    
    except Exception as e:
        return {
        "status": False,
        "message": str(e)
    }



@router.post("/edit_check_document/{user_id}")
def edit_check_document(
    user_id :int, 
    field:  str = Body(...),
    value:  str = Body(...), 
    db: Session = Depends(get_db)):
    try:
   
        result = service_document.edit_check_document(db,field, value,user_id)
    
        return {
            "success": True,
            "data": result
        }
    
    except Exception as e:
        return {
        "status": False,
        "message": str(e)
    }