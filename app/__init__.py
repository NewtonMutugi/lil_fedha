# app/__init__.py
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from app.config import SQLALCHEMY_DATABASE_URI
from app.config import SQLALCHEMY_TRACK_MODIFICATIONS
from app.config import SECRET_KEY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = SECRET_KEY
api = Api(app)
jwt = JWTManager(app)

# Initialize the database

# Import routes here (see next step)
