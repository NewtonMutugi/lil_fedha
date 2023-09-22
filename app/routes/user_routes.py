# app/routes/user_routes.py
from datetime import datetime, timedelta, timezone
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, get_jwt, jwt_required, create_access_token, get_jwt_identity
from app.common import db, hash_password, verify_password
from app.models import TokenBlocklist, User


user_blueprint = Blueprint('user', __name__)
api = Api(user_blueprint)


# Callback function to check if a JWT exists in the database blocklist

class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("email", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        parser.add_argument("first_name", type=str, required=True)
        parser.add_argument("last_name", type=str, required=True)
        args = parser.parse_args()

        # Hash the password before saving it in the database (you should use a secure hashing method)
        password_hash = hash_password(args["password"])

        user = User(
            username=args["username"],
            email=args["email"],
            password_hash=password_hash,
        )

        db.session.add(user)
        db.session.commit()
        return {"message": "User registered successfully"}, 201


class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
        args = parser.parse_args()

        # Verify the username and password
        user = User.query.filter_by(username=args["username"]).first()
        if user and verify_password(args["password"], user.password_hash):
            access_token = create_access_token(identity=user.user_id)
            return {"jwt_token": access_token}, 200
        else:
            return {"message": "Invalid credentials"}, 401

class UserLogout(Resource):
    @jwt_required()
    def delete(self):
        # Get the raw JWT token from the request
        raw_jwt = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=raw_jwt, created_at=now))
        db.session.commit()
        return {"message": "User logged out successfully"}, 200

class UserProfile(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user:
            # Return user profile data
            return {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        else:
            return {"message": "User not found"}, 404

    @jwt_required()
    def put(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user:
            parser = reqparse.RequestParser()
            parser.add_argument("first_name", type=str)
            parser.add_argument("last_name", type=str)
            args = parser.parse_args()

            # Update user profile data
            user.first_name = args["first_name"] or user.first_name
            user.last_name = args["last_name"] or user.last_name
            db.session.commit()
            return {"message": "User profile updated successfully"}, 200
        else:
            return {"message": "User not found"}, 404


api.add_resource(UserRegister, "/api/user/register")
api.add_resource(UserLogin, "/api/user/login")
api.add_resource(UserProfile, "/api/user/profile")
api.add_resource(UserLogout, "/api/user/logout")

