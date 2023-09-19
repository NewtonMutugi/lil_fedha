# app/common.py
from datetime import timedelta
from flask import Blueprint
from flask_jwt_extended import JWTManager
from flask_restful import Api
from passlib.hash import pbkdf2_sha256
from flask_sqlalchemy import SQLAlchemy


common_blueprint = Blueprint('common', __name__)
common_api = Api(common_blueprint)
db = SQLAlchemy()



def init_app(app):
    db.init_app(app)

# Function to hash a password
def hash_password(password):
    return pbkdf2_sha256.hash(password)

# Function to verify a password
def verify_password(plain_password, hashed_password):
    return pbkdf2_sha256.verify(plain_password, hashed_password)



