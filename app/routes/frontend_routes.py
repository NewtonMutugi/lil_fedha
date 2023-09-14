from flask import Blueprint, render_template


frontend_blueprint = Blueprint('frontend', __name__, url_prefix='/')



@frontend_blueprint.route('/')
def index():
    return "Hello world"
@frontend_blueprint.route('/about')
def about():
    return "About us"

@frontend_blueprint.route('/login', methods=['GET'])
def login():
    return render_template("log_in.html")

@frontend_blueprint.route('sign_up', methods=['POST', 'GET'])
def sign_up():
    return render_template("sign_up.html")
