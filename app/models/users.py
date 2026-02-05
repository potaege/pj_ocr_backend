from sqlalchemy import text
from sqlalchemy.orm import Session
from app.entities.users import User


def get_all_users(db: Session):
    sql = text("""
        SELECT
            user_id,
            username,
            email,
            name,
            surname,
            created_at,
            updated_at
        FROM users
        ORDER BY user_id DESC
    """)
    return db.execute(sql).mappings().all()


def get_user_by_id(db: Session, user_id: int):
    sql = text("""
        SELECT
            user_id,
            username,
            email,
            name,
            surname,
            created_at,
            updated_at
        FROM users
        WHERE user_id = :user_id
        LIMIT 1
    """)

    return db.execute(sql, {
                "user_id": user_id
            }).mappings().first()

def get_user_by_id_all_data(db:Session,username:str):

    return db.query(User).filter(User.username == username).first()

