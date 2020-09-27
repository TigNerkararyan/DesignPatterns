from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField

class RegisterForm(FlaskForm):
    username = StringField("Username")
    email = StringField("Email")
    password = PasswordField("Password")
    check = BooleanField("isAdmin")

class EventForm(FlaskForm):
    date = StringField("datepicker")