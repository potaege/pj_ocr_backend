from fastapi import APIRouter , Depends
from pydantic import BaseModel

from sqlalchemy.orm import Session
from app.db.deps import get_db
import app.services.document as service_document
import app.services.thai_id as service_thai_id


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
