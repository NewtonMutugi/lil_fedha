# app/routes/expenses_routes.py
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import jwt_required
from app.common import db
from app.models import ExpensesCategories

expenses_blueprint = Blueprint('expenses', __name__)
api = Api(expenses_blueprint)

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

api.add_resource(ExpensesCategoriesResource, "/api/expenses/categories")
