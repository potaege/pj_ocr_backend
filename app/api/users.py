from fastapi import APIRouter , Depends
from pydantic import BaseModel

from sqlalchemy.orm import Session
from app.db.deps import get_db
import app.services.users as service_users



router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def root():
    return {"message": "users is ok"}

@router.get("/getList")
def list_users(db: Session = Depends(get_db)):
   

    return service_users.list_users(db)


@router.get("/getUser/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:

        data = service_users.get_user_by_id(db, user_id)

        return {
            "status": True,
            "data": data
        }
    
    except Exception as e:
        return {
        "status": False,
        "message": str(e)
    }



