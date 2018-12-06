from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Customer


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class CreateCustomerForm(FlaskForm):
    customer_name = StringField('Customer name', validators=[DataRequired()])
    customer_email = StringField('Email', validators=[Email()])
    customer_company = StringField('Company name')
    customer_phone = StringField('Phone number')
    customer_address = TextAreaField()
    submit = SubmitField('Create Customer')

    def validate_email(self, email):
        customer = Customer.query.filter_by(customer_email=customer_email.data).first()
        if customer is not None:
            raise ValidationError('Please use a different email address.')
