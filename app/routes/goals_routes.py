# app/routes/goals_routes.py
from datetime import datetime
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.common import db
from app.models import SavingGoals

goals_blueprint = Blueprint('goals', __name__)
api = Api(goals_blueprint)

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

api.add_resource(SavingGoalsResource, "/api/goals")
