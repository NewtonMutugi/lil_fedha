# app/__init__.py
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
# from app.common import init_app
from app.config import ACCESS_EXPIRES, SQLALCHEMY_DATABASE_URI
from app.config import SQLALCHEMY_TRACK_MODIFICATIONS
from app.config import SECRET_KEY
from app.models import TokenBlocklist
from app.routes.user_routes import user_blueprint
from app.routes.expenses_routes import expenses_blueprint
from app.routes.goals_routes import goals_blueprint
from app.common import common_blueprint, init_app
from app.routes.frontend_routes import frontend_blueprint
from app.common import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = SECRET_KEY

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
api = Api(app)
jwt = JWTManager(app)


# Initialize the app with common configurations
init_app(app)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None

# Register your blueprints
app.register_blueprint(common_blueprint)  # Register the common blueprint
app.register_blueprint(user_blueprint, url_prefix='/')
app.register_blueprint(expenses_blueprint, url_prefix='/expenses')
app.register_blueprint(goals_blueprint, url_prefix='/goals')
app.register_blueprint(frontend_blueprint, url_prefix='/app')
