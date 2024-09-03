from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import MetaData
from flask_restful import Api, Resource
from flask import request, make_response, jsonify
import os


app = Flask(__name__)
CORS(app)

metadata = MetaData()
app.json.compact = False

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URI', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
api = Api(app)
db.init_app(app)