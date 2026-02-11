from sqlalchemy import text
from sqlalchemy.orm import Session
from app.entities.passport import Passport 
from sqlalchemy.exc import IntegrityError

def get_passport_by_user(db: Session, user_id : int):

    return db.query(Passport).filter(Passport.user_id == user_id).first()


def add_passport(db: Session, data: dict) -> Passport:
    
    passport = Passport(**data)

    try:
        db.add(passport)
        db.commit()
        
        return True
    
    except IntegrityError:
        db.rollback()
        raise ValueError("passport already exists")
    
def edit_passport(db: Session, user_id: int, data: dict) -> bool:

    passport = db.query(Passport).filter_by(user_id=user_id).first()

    if not passport:
        raise ValueError("ThaiID not found")

    try:
        for key, value in data.items():
            setattr(passport, key, value)

        db.commit()
        db.refresh(passport)

        return True

    except IntegrityError:
        db.rollback()
        raise ValueError("Citizen ID already exists")

    