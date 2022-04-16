from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256
from models import User


def invaild_credentials(form, field):
    username_entered = form.username.data
    password_entered = field.data

    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError("Nazwa konta lub hasło jest nieprawidłowe")
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Nazwa konta lub hasło jest nieprawidłowe")


class RegistrationForm(FlaskForm):
    
    username = StringField('username_label', validators=[InputRequired(message="Pole użytkownika jest wymagane"), Length(min=4, max=25, message="Username must be between 4 and 25 chars")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), Length(min=4, max=25, message="Password must be between 4 and 25 chars")])
    confirm_pass = PasswordField('confirm_pass_label', validators=[InputRequired(message="Password required"), EqualTo('password', message="Passwords must match")])
    submit_button = SubmitField('Create')

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Konto o tej nazwie juz istnieje, wybierz inne konto")

class LoginForm(FlaskForm):
    username = StringField('username_label', validators=[InputRequired(message="Pole użytkownika jest wymagane")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), invaild_credentials])
    submit_button = SubmitField('Login')