# run.py
from flask_sqlalchemy import SQLAlchemy
from app import app
from app import init_app




if __name__ == '__main__':
    app.run(debug=True)
