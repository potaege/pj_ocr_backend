import app.models.users as model_users

def list_users(db):
    return model_users.get_all_users(db)

def get_user_by_id(db , id):

    return model_users.get_user_by_id(db ,id)
