# app/routes/__init__.py

from flask import Blueprint
from flask_restful import Api
from .user_routes import user_blueprint
from .expenses_routes import expenses_blueprint
from .goals_routes import goals_blueprint
from .frontend_routes import frontend_blueprint


common_blueprint = Blueprint('common', __name__)
common_api = Api(common_blueprint)
