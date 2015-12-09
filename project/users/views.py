from flask import flash, redirect, render_template, request, url_for, Blueprint
from flask.ext.login import login_user, login_required, logout_user, \
                            current_user
from .forms import LoginForm, RegisterForm
from project import db, bcrypt
from project.models import User

users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
)

def new_user(name, email, password):
    user = User(
        name=name,
        email=email.lower(),
        password=bcrypt.generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()
    return user

@users_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        flash('You are already logged in.')
        return redirect(url_for('home.home'))
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None:
                error = 'Invalid username or password.'
            elif bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('You were successfully logged in.')
                next_url = request.args.get('next')
                return redirect(next_url or url_for('home.home'))
            else:
                error = 'Invalid username or password.'
    return render_template('login.html', form=form, error=error)

@users_blueprint.route('/logout/')
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('home.home'))

@users_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = new_user(form.name.data, form.email.data, form.password.data)
        login_user(user)
        return redirect(url_for('home.home'))
    return render_template('register.html', form=form)
