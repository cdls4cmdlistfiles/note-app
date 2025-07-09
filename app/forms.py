from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from .models import User

class LoginForm(FlaskForm):
    username = StringField('Username', 
    validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('Username does not exist. Please register first.')

    def validate_password(self, password):
        if 'username' in self.__dict__:  # Only validate password if username is valid
            user = User.query.filter_by(username=self.username.data).first()
            if user and not user.check_password(password.data):
                raise ValidationError('Incorrect password. Please try again.')

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
    validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(),
    Length(min=8, max=30, message='Password must be between 8 and 30 characters long')
    ])
    confirm_password = PasswordField('Confirm Password',
    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')
    