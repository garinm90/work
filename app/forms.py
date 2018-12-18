from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, \
    MultipleFileField, IntegerField, widgets
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, NumberRange
from app.models import User, Customer


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


