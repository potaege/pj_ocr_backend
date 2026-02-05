from fastapi import APIRouter , Depends
from pydantic import BaseModel

from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.auth import LoginRequest
import app.services.users as service_users

router = APIRouter(prefix="/login", tags=["login"])


@router.post("/check_login")
def check_login(
    payload: LoginRequest,
    db: Session = Depends(get_db)
):
    try:

        data = service_users.service_login(db, payload)

        return {
            "status": True,
            "user_id": data
        }
    
    except Exception as e:
        return {
        "status": False,
        "message": str(e)
    }

