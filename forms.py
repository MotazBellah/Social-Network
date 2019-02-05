from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email
                                Length, EqualTo)
from models import User

# Function to check if the name already in exists
def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User already exists.')

# Function to check if the email already in exists
email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User already exists.')

# Create the Registeration class that contaoins username, email, password, password2
class RegisterForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message='''Username should be one word,
                        letters, numbers, and underscores only'''
            ),
            name_exists
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6),
            EqualTo('password2', message="Password must match")
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )
