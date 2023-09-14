# run.py
from flask_sqlalchemy import SQLAlchemy
from app import app
from app.common import init_app




if __name__ == '__main__':
    app.run(debug=True, ssl_context="adhoc")
