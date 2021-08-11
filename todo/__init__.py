import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from json import JSONEncoder
from oauthlib.oauth2 import WebApplicationClient


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

google_client_id = os.environ['GOOGLE_CLIENT_ID']
google_client_secret = os.environ['GOOGLE_CLIENT_SECRET']
client = WebApplicationClient(google_client_id)
openid_config_file_name = "google_openid_configs.json"

db = SQLAlchemy(app)

from . import routes
