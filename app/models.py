from flask_login import UserMixin
from .firestore_service import get_user


class UserData:
  def __init__(self, fullname, password):
    self.fullname = fullname
    self.password = password

class UserModel(UserMixin):
  def __init__(self, user_data):
    """
    :param user_data: UserData
    """
    self.id = user_data.fullname
    self.password = user_data.password

  @staticmethod
  def query(user_id): 
    user_doc = get_user(user_id)
    user_data = UserData(
      fullname= user_doc.id,
      password= user_doc.to_dict()['password']
    )
    return UserModel(user_data)