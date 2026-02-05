from sqlalchemy import text
from sqlalchemy.orm import Session
from app.entities.passport import Passport 
from sqlalchemy.exc import IntegrityError

def get_passport_by_user(db: Session, user_id : int):

    return db.query(Passport).filter(Passport.user_id == user_id).first()