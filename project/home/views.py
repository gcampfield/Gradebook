from flask import flash, redirect, render_template, request, url_for, Blueprint
from flask.ext.login import login_user, login_required, logout_user

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)

@home_blueprint.route('/')
def home():
    return render_template('index.html')
