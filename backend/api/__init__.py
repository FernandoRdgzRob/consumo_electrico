from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# Use this file to change the uri from the database that is going to be used across the system

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://ec_user:12341234@localhost/electrical_consumption"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
