from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, \
    MultipleFileField, FileField, IntegerField, widgets
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Customer, Order


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
    name = StringField('Customer name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    company = StringField('Company name')
    phone = StringField('Phone number')
    address = TextAreaField()
    submit = SubmitField('Create Customer')

    def validate_email(self, email):
        customer = Customer.query.filter_by(email=email.data).first()
        if customer is not None:
            raise ValidationError('Please use a different email address.')


class DeleteForm(FlaskForm):
    delete = SubmitField('Delete')


class CreateOrderForm(FlaskForm):
    bubble_six = BooleanField()
    bubble_nine = BooleanField()
    bubble_fourteen = BooleanField()
    puck_six = BooleanField()
    puck_molex_six = BooleanField()
    puck_nine = BooleanField()
    long_nineteen = BooleanField()
    short_nineteen = BooleanField()
    green_nineteen = BooleanField()
    ads_twentyfour = BooleanField()
    ads_thirtysix = BooleanField()
    customer_id = SelectField('Customer', coerce=int)
    submit = SubmitField('Create Order')
    two_forty = BooleanField("Two Forty")
    three_twenty = BooleanField("Three Twenty")


class ImageUploadForm(FlaskForm):
    images = MultipleFileField('Upload Images', id='images')
    order = SelectField('Order')
    submit = SubmitField('Upload')


class QuoteForm(FlaskForm):
    # Lights
    bubble_six = IntegerField('Bubble 6', widget=widgets.Input(input_type='number'), default=0)
    bubble_nine = IntegerField('Bubble 9', widget=widgets.Input(input_type='number'), default=0)
    bubble_fourteen = IntegerField('Bubble 14', widget=widgets.Input(input_type='number'), default=0)
    puck_six = IntegerField('Puck 6', widget=widgets.Input(input_type='number'), default=0)
    puck_molex_six = IntegerField('Puck 6 Molex', widget=widgets.Input(input_type='number'), default=0)
    puck_nine = IntegerField('Puck 9', widget=widgets.Input(input_type='number'), default=0)
    long_nineteen = IntegerField('Long Wire 19', widget=widgets.Input(input_type='number'), default=0)
    short_nineteen = IntegerField('Short Wire 19', widget=widgets.Input(input_type='number'), default=0)
    green_nineteen = IntegerField('Green 19', widget=widgets.Input(input_type='number'), default=0)
    ads_twentyfour = IntegerField('ADS 24', widget=widgets.Input(input_type='number'), default=0)
    ads_thirtysix = IntegerField('ADS 36', widget=widgets.Input(input_type='number'), default=0)
    submit = SubmitField('Submit')

    # Power Supplies
    two_forty = IntegerField('240', widget=widgets.Input(input_type='number'), default=0)
    three_twenty = IntegerField('320', widget=widgets.Input(input_type='number'), default=0)
