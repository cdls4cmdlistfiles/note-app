

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
import os
from dotenv import load_dotenv

migrate = Migrate()
db = SQLAlchemy()
moment = Moment()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

load_dotenv()  # loads variables from .env into environment

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db_path = os.path.join(os.path.dirname(__file__), '../database.db')
app.config['SECRET_KEY'] = '%&F^*GH()J'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///tmp/{db_path}'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
moment.init_app(app)


from .models import User

from app.auth import app as auth
app.register_blueprint(auth)

from app.views import app as views
app.register_blueprint(views)
