# app/models.py
from flask import app
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
from app.common import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))

class FinancialData(db.Model):
    data_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("expenses_categories.category_id"), nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)

class ExpensesCategories(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    category_description = db.Column(db.Text)

class SavingsPlan(db.Model):
    savings_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    plan_name = db.Column(db.String(100), nullable=False)
    monthly_contribution = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.DateTime)
    duration = db.Column(db.Integer, nullable=False)

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)
