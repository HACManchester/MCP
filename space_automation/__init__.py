from flask import Flask
from space_automation.mod_auth.controllers import mod_auth
from flask_login import LoginManager

app = Flask(__name__)
app.register_blueprint(mod_auth)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        return mod_auth.models.User.get(mod_auth.models.User.id == user_id)
    except mod_auth.models.User.DoesNotExist:
        return None
