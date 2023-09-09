from datetime import datetime
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///your_database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your_secret_key"
api = Api(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)  # Moved SQLAlchemy initialization here

# ...

# Function to hash a password
def hash_password(password):
    return pbkdf2_sha256.hash(password)

# Function to verify a password
def verify_password(plain_password, hashed_password):
    return pbkdf2_sha256.verify(plain_password, hashed_password)

# Define other tables (FinancialData, ExpensesCategories, SavingGoals) similarly

# Create database tables
with app.app_context():
    db.create_all()

# Now you can import the models after db initialization
# from models import ExpensesCategories, SavingGoals, User

# User registration and authentication
class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", type=str, required=True)
        parser.add_argument("email", type=str, required=True)
        parser.add_argument("password", type=str, required=True)
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
            return {"access_token": access_token}, 200
        else:
            return {"message": "Invalid credentials"}, 401


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

class ExpensesCategoriesResource(Resource):
        @jwt_required()
        def get(self):
            categories = ExpensesCategories.query.all()
            return [
                {
                    "category_id": category.category_id,
                    "category_name": category.category_name,
                    "category_description": category.category_description,
                }
                for category in categories
            ]

        @jwt_required()
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument("category_name", type=str, required=True)
            parser.add_argument("category_description", type=str)
            args = parser.parse_args()

            category = ExpensesCategories(
                category_name=args["category_name"],
                category_description=args["category_description"],
            )

            db.session.add(category)
            db.session.commit()
            return {"message": "Expense category added successfully"}, 201

class SavingGoalsResource(Resource):
        @jwt_required()
        def get(self):
            current_user_id = get_jwt_identity()
            goals = SavingGoals.query.filter_by(user_id=current_user_id).all()
            return [
                {
                    "goals_id": goal.goals_id,
                    "goal_name": goal.goal_name,
                    "target_amount": goal.target_amount,
                    "current_amount": goal.current_amount,
                    "due_date": goal.due_date.strftime("%Y-%m-%d %H:%M:%S"),
                }
                    for goal in goals
                ]

        @jwt_required()
        def post(self):
            current_user_id = get_jwt_identity()
            parser = reqparse.RequestParser()
            parser.add_argument("goal_name", type=str, required=True)
            parser.add_argument("target_amount", type=float, required=True)
            parser.add_argument("due_date", type=str)
            args = parser.parse_args()

            try:
                due_date = datetime.strptime(args["due_date"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return {"message": "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'."}, 400

            goal = SavingGoals(
                user_id=current_user_id,
                goal_name=args["goal_name"],
                target_amount=args["target_amount"],
                due_date=due_date,
                current_amount=0.0,  # Initialize current amount to 0
            )

            db.session.add(goal)
            db.session.commit()
            return {"message": "Saving goal added successfully"}, 201



# Add API routes
api.add_resource(UserRegister, "/api/user/register")
api.add_resource(UserLogin, "/api/user/login")
api.add_resource(UserProfile, "/api/user/profile")
api.add_resource(ExpensesCategoriesResource, "/api/expenses/categories")
api.add_resource(SavingGoalsResource, "/api/goals")

# Add routes for Financial Data, Goals, etc. similarly


if __name__ == "__main__":
    app.run(debug=True)
