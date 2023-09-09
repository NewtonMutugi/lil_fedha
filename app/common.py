# app/common.py
from flask import app
from passlib.hash import pbkdf2_sha256
from models import db

# ... (common functions)
def hashpass(password):
    return pbkdf2_sha256.hash(password)

def checkpass(password, hash):
    return pbkdf2_sha256.verify(password, hash)

db.init_app(app)
