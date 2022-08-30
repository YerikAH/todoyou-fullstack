from flask import Flask
from .config import Config
from flask_login import LoginManager
from .models import UserModel

login_manager = LoginManager()
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id=''):
    return None

@login_manager.user_loader
def load_user(fullname):
  return UserModel.query(fullname)


def create_app():
  app = Flask(
    __name__,
    template_folder='./templates',
    static_folder='./static'
  )
  app.config.from_object(Config)
  login_manager.init_app(app)

  
  return app