from app.views.formatter import format

import app.models.thai_id as model_thai_id


def get_thai_id_by_user(db, user_id):

    data = model_thai_id.get_thai_id_by_user(db,user_id)

    data = format(data,"thai_id","full")

    return data


def add_thai_id(db , data: dict):

    exists = model_thai_id.get_thai_id_by_user(db,data["user_id"])
    if exists:
        raise ValueError("Thai ID for this user already exists")

    add_data = model_thai_id.add_thai_id(db,data)

    return add_data