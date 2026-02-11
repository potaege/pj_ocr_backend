from sqlalchemy import text
from sqlalchemy.orm import Session
from app.entities.house_registration import HouseRegistration 
from sqlalchemy.exc import IntegrityError

def get_house_registration_by_user(db: Session, user_id : int):

    return db.query(HouseRegistration).filter(HouseRegistration.user_id == user_id).all()

def get_house_registration_by_id(db: Session, id : int):

    return db.query(HouseRegistration).filter(HouseRegistration.id == id).first()

def add_house_registration(db: Session, data: dict) -> HouseRegistration:
    
    house_registration = HouseRegistration(**data)

    try:
        db.add(house_registration)
        db.commit()
        
        return True
    
    except IntegrityError:
        db.rollback()
        raise ValueError("house registration already exists")
    
def edit_house_registration(db: Session, id: int, data: dict) -> bool:

    house_registration = db.query(HouseRegistration).filter(HouseRegistration.id == id).first()
    if not house_registration:
        raise ValueError("HouseRegistration not found")

    try:
        for key, value in data.items():
            setattr(house_registration, key, value)

        db.commit()
        db.refresh(house_registration)

        return True

    except IntegrityError:
        db.rollback()
        raise ValueError("HouseRegistration already exists")