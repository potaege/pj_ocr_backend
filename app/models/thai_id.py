from sqlalchemy import text
from sqlalchemy.orm import Session
from app.entities.thai_id import ThaiID 
from sqlalchemy.exc import IntegrityError

def get_thai_id_by_user(db: Session, user_id : int):

    return db.query(ThaiID).filter(ThaiID.user_id == user_id).first()


def add_thai_id(db: Session, data: dict) -> ThaiID:
    
    thai_id = ThaiID(**data)

    try:
        db.add(thai_id)
        db.commit()
        
        return True
    
    except IntegrityError:
        db.rollback()
        raise ValueError("Citizen ID already exists")
    

def edit_thai_id(db: Session, user_id: int, data: dict) -> bool:

    thai_id = db.query(ThaiID).filter_by(user_id=user_id).first()

    if not thai_id:
        raise ValueError("ThaiID not found")

    try:
        for key, value in data.items():
            setattr(thai_id, key, value)

        db.commit()
        db.refresh(thai_id)

        return True

    except IntegrityError:
        db.rollback()
        raise ValueError("Citizen ID already exists")


