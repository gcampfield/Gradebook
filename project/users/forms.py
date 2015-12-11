from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from project.models import User

class LoginForm(Form):
    email = TextField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(Form):
    firstname = TextField(
        'First',
        validators=[DataRequired(), Length(min=3, max=25)]
    )

    lastname = TextField(
        'Last',
        validators=[DataRequired(), Length(min=3, max=25)]
    )

    email = TextField(
        'Email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )

    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(), EqualTo('password', message='Passwords must match.')
        ]
    )

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user:
          self.email.errors.append('That email is already taken')
          return False

        return True
