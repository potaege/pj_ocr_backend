from sqlalchemy import text
from sqlalchemy.orm import Session
from app.entities.driving_licence import DrivingLicence 
from sqlalchemy.exc import IntegrityError


def get_driving_licence_by_user(db: Session, user_id : int):

    return db.query(DrivingLicence).filter(DrivingLicence.user_id == user_id).all()

def get_driving_licence_by_id(db: Session, id : int):
    return db.query(DrivingLicence).filter(DrivingLicence.id == id).first()


def add_driving_licence(db: Session, data: dict) -> DrivingLicence:
    
    driving_licence = DrivingLicence(**data)

    try:
        db.add(driving_licence)
        db.commit()
        
        return True
    
    except IntegrityError:
        db.rollback()
        raise ValueError("DrivingLicence already exists")
    
def edit_driving_licence(db: Session, id: int, data: dict) -> bool:

    driving_licence = db.query(DrivingLicence).filter(DrivingLicence.id == id).first()
    if not driving_licence:
        raise ValueError("DrivingLicence not found")

    try:
        for key, value in data.items():
            setattr(driving_licence, key, value)

        db.commit()
        db.refresh(driving_licence)

        return True

    except IntegrityError:
        db.rollback()
        raise ValueError("DrivingLicence already exists")