from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from project.models import User

class LoginForm(Form):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(Form):
    firstname = TextField(
        'First',
        validators=[DataRequired(), Length(min=1, max=30)]
    )

    lastname = TextField(
        'Last',
        validators=[DataRequired(), Length(min=1, max=30)]
    )

    email = EmailField(
        'Email',
        validators=[DataRequired(),
                    Email(message="Please enter a valid email address"),
                    Length(min=6, max=40)]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )

    confirm = PasswordField(
        'Confirm',
        validators=[
            DataRequired(), EqualTo('password', message='Passwords must match.')
        ]
    )

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(email=self.email.data.lower()).first()
        if user:
          self.email.errors.append('That email is already taken.')
          return False

        return True
