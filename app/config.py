# config.py
from datetime import datetime, timedelta

SQLALCHEMY_DATABASE_URI = "sqlite:///your_database.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "your_secret_key"
ACCESS_EXPIRES = timedelta(hours=1)
BASE_URL = "http://127.0.0.1:5000"
