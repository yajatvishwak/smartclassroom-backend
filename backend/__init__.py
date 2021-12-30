
from flask import Flask 
import os

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow


currentDirectory = os.path.dirname(os.path.abspath(__file__))


app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)
ma = Marshmallow(app)

from backend import routes
from backend import models
