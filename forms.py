from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import Length, Email, ValidationError, InputRequired


class NewUserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=20, message='Username must be 3 to 20 characters')])
    password = StringField('Password', validators=[InputRequired(), Length(max=55, min=6)])
    email = EmailField('Email', validators=[InputRequired(), Length(max=50), Email()])
    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30, message='Name must be less than 30 characters')])
    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30, message='Name must be less than 30 characters')])


class UserLoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(max=20, min=3)])
    password = PasswordField('Password', validators=[InputRequired(), Length(max=55, min=6)])

class FeedbackForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """Delete form"""
