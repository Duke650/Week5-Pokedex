from flask import Flask
from config import Config
from flask_login import LoginManager
from app.models import User, db
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()

login_manager.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)

@login_manager.user_loader
def loadUser(userID):
    return User.query.get(userID)


from app import routes