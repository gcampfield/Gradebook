from flask import Blueprint, redirect, render_template, url_for
from flask.ext.login import current_user

home_blueprint = Blueprint(
    'home', __name__,
    template_folder='templates'
)

@home_blueprint.route('/')
def home():
    if current_user.is_authenticated():
        return redirect(url_for('grades.dashboard'))
    return render_template('index.html')
