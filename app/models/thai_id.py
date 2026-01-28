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
    

