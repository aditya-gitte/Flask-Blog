from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from db import db


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = db.users.count_documents({"username": username.data})
        # print(user)
        # print(username)
        # print(username.data)
        if user != 0:
            raise ValidationError('That username is already taken ')

    def validate_email(self, email):
        useremailcount = db.users.count_documents({"email": email.data})
        # print(useremailcount)
        if useremailcount != 0:
            raise ValidationError('That email is already taken ')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class BlogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    blog_des = StringField('Blog', validators=[DataRequired()])
    submit = SubmitField('Publish')
