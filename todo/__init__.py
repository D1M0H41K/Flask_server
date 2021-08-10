import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        return str(o)


load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace('postgres', 'postgresql')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.json_encoder = CustomJSONEncoder
login_manager = LoginManager()
login_manager.init_app(app=app)

db = SQLAlchemy(app)

from . import routes
