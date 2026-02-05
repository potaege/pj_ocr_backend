from sqlalchemy import text
from sqlalchemy.orm import Session
from app.entities.house_registration import HouseRegistration 
from sqlalchemy.exc import IntegrityError

def get_house_registration_by_user(db: Session, user_id : int):

    return db.query(HouseRegistration).filter(HouseRegistration.user_id == user_id).all()