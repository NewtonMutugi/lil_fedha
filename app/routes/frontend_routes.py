# app/routes/frontend_routes.py
from flask import Blueprint, flash, jsonify, make_response, redirect, render_template, request, url_for
from flask_jwt_extended import set_access_cookies
import requests

from app.forms import LoginForm, SignupForm


frontend_blueprint = Blueprint('frontend', __name__, url_prefix='/')


@frontend_blueprint.route('/')
def index():
    return "Hello world"


@frontend_blueprint.route('/about')
def about():
    return "About us"


@frontend_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    user = None
    form = LoginForm()
    if form.validate_on_submit():
        # Create a JSON object with the user credentials
        user_data = {
            "username": form.username.data,
            "password": form.password.data
        }
        print(user_data)
        # Send a POST request to the local Flask endpoint `/api/user/login`
        headers = {'Content-Type': 'application/json'}
        response = requests.post("http://localhost:5000/api/user/login", json=user_data)
        print(response)

        # If the login is successful, store the JWT authorization token in a cookie
        if response.status_code == 200:
            # Authentication successful, store the JWT token in a cookie
            jwt_token = response.json().get('jwt_token')
            resp = make_response(render_template("dashboard.html", form=form, user=user))
            resp.set_cookie('jwt_token', jwt_token)
            # set_access_cookies(response=response, encoded_access_token=jwt_token)
            return render_template("dashboard.html",form=form,user=user)

        # If the login is unsuccessful, prompt the user that the login credentials are incorrect
        elif response.status_code == 401:
            flash('Incorrect login credentials.')
            return redirect(url_for('frontend.login'))

    return render_template("log_in.html", form=form, user=user)




@frontend_blueprint.route('sign_up', methods=['POST', 'GET'])
def sign_up():
    form = SignupForm()
    if form.validate_on_submit():
        user_data = {
            "username": form.username.data,
            "email": form.email.data,
            "password": form.password.data,
            "first_name": form.first_name.data,
            "last_name": form.last_name.data,
            "date_of_birth": str(form.date_of_birth.data)
        }
        response = requests.post("http://localhost:5000/api/user/register", json=user_data)
        print(response)

        if response.status_code == 201:
            flash('You have successfully signed up!')
            redirect(url_for('frontend.login'))
        else:
            flash('Something went wrong. Please try again.')
            redirect(url_for('frontend.sign_up'))
    return render_template("sign_up.html", form=form)


@frontend_blueprint.route('dashboard', methods=['POST', 'GET'])
def dashboard():
    return render_template("dashboard.html")


@frontend_blueprint.route('profile', methods=['POST', 'GET'])
def profile():
    return render_template("profile.html")


@frontend_blueprint.route('bills', methods=['POST', 'GET'])
def bills():
    return render_template("bills.html")


@frontend_blueprint.route('savings', methods=['POST', 'GET'])
def savings():
    return render_template("savings.html")
