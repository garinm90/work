from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, \
    MultipleFileField, FileField, IntegerField, widgets
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, NumberRange
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

    def __init__(self, original_email, *args, **kwargs):
        super(CreateCustomerForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            customer = Customer.query.filter_by(email=self.email.data).first()
            if customer is not None:
                raise ValidationError('Please use a different email address.')


class DeleteForm(FlaskForm):
    delete = SubmitField('Delete')


class CreateOrderForm(FlaskForm):
    bubble_six = IntegerField(widget=widgets.Input(input_type='number'), default=0,
                              validators=[NumberRange(min=0, max=1000000)])
    bubble_nine = IntegerField(widget=widgets.Input(input_type='number'), default=0,
                               validators=[NumberRange(min=0, max=1000000)])
    bubble_fourteen = IntegerField(widget=widgets.Input(input_type='number'), default=0,
                                   validators=[NumberRange(min=0, max=1000000)])
    puck_six = IntegerField(widget=widgets.Input(input_type='number'), default=0,
                            validators=[NumberRange(min=0, max=1000000)])
    puck_molex_six = IntegerField(widget=widgets.Input(input_type='number'), default=0,
                                  validators=[NumberRange(min=0, max=1000000)])
    puck_nine = IntegerField(widget=widgets.Input(input_type='number'), default=0,
                             validators=[NumberRange(min=0, max=1000000)])
    long_nineteen = IntegerField(widget=widgets.Input(input_type='number'), default=0,
                                 validators=[NumberRange(min=0, max=1000000)])
    short_nineteen = IntegerField(widget=widgets.Input(input_type='number'), default=0,
                                  validators=[NumberRange(min=0, max=1000000)])
    green_nineteen = IntegerField(widget=widgets.Input(input_type='number'), default=0,
                                  validators=[NumberRange(min=0, max=1000000)])
    ads_twentyfour = IntegerField(widget=widgets.Input(input_type='number'), default=0,
                                  validators=[NumberRange(min=0, max=1000000)])
    ads_thirtysix = IntegerField(widget=widgets.Input(input_type='number'), default=0,
                                 validators=[NumberRange(min=0, max=1000000)])
    customer_id = SelectField('Customer', coerce=int)
    submit = SubmitField('Submit Order')
    two_forty = IntegerField(widget=widgets.Input(input_type='number'), default=0,
                             validators=[NumberRange(min=0, max=1000000)])
    three_twenty = IntegerField(widget=widgets.Input(input_type='number'), default=0,
                                validators=[NumberRange(min=0, max=1000000)])
    ride = StringField('Ride Name:')


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
