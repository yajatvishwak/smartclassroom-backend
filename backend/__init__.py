
from flask import Flask , request
import os

from flask_sqlalchemy import SQLAlchemy

currentDirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://///mnt/a150bccb-ca02-44eb-bda7-a3ae046d1095/College/Coding/Third Year/vibha/backend/backend/test.db"
db = SQLAlchemy(app)

from backend import routes
from backend import models
