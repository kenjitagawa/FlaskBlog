from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from pyblog.models import User

class RegistrationForm(FlaskForm):
    
    """
    The registration form will take the information from the form in the HTML and process the information. Here it takes the following fields: 
    - Username
    - Email
    - Password
    - Password Confirmation
    - Submit Button
    
    It also contains the two following methods:
    - validate_username => expects username
    - validate_email => expects email
    """
    
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        
        if user:
            raise ValidationError('That username is not available. Please choose another one.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        
        if email:
            raise ValidationError('That email is taken. Please choose another one.')

class LoginForm(FlaskForm):
    
    """
    The LoginForm class will take the information from the form in the HTML and process the information. Here it takes the following fields: 
    - Email
    - Password
    - Remember Me
    - Submit Button
    """
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class UpdateAccountForm(FlaskForm):
    
    """
    The UpdateAccForm class will take the information from the form in the HTML and process the information. Here it takes the following fields: 
    - Username
    - Email
    - Picture
    - Submit Button
    
    It also contains the two following methods:
    - validate_username => expects username
    - validate_email => expects email
    """
    
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        # Check for a different username
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            
            if user:
                raise ValidationError('That username is not available. Please choose another one.')

    def validate_email(self, email):
        # Check for a different email
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            
            if email:
                raise ValidationError('That email is taken. Please choose another one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Send Me An Email!')
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        
        if email is None:
            raise ValidationError('That email doesn\'t have an account!')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('Reset Password')
