from sqlalchemy import text
from sqlalchemy.orm import Session
from app.entities.driving_licence import DrivingLicence 
from sqlalchemy.exc import IntegrityError


def get_driving_licence_by_user(db: Session, user_id : int):

    return db.query(DrivingLicence).filter(DrivingLicence.user_id == user_id).all()