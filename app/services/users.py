import app.models.users as model_users

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.auth import LoginRequest
from app.models.users import User
# from passlib.hash import bcrypt entities

def list_users(db):
    return model_users.get_all_users(db)

def get_user_by_id(db , id):

    return model_users.get_user_by_id(db ,id)


def service_login(db: Session, payload: LoginRequest):
    user = model_users.get_user_by_id_all_data(db, payload.username)

    if not user:
        raise HTTPException(status_code=400, detail="ไม่พบบัญชีผู้ใช้")

    # if not bcrypt.verify(payload.password, user.password):
    #     raise HTTPException(status_code=400, detail="รหัสผ่านไม่ถูกต้อง")

    if(payload.password != user.password):
        raise HTTPException(status_code=400, detail="รหัสผ่านไม่ถูกต้อง")

    return user.user_id
       
    