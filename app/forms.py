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


class CreateControllerForm(FlaskForm):
    order_id = SelectField('Order', coerce=int)
    customer_id = SelectField('Customer', coerce=int)
    t_one_thousand = StringField('T1000', default=0, validators=[DataRequired()])
    t_one_thousand_a = StringField('T1000A', default=0, validators=[DataRequired()])
    ym_four = StringField('YM-4', default=0, validators=[DataRequired()])
    ym_eight = StringField('YM-8', default=0, validators=[DataRequired()])
    falcon_two = StringField('F2', default=0, validators=[DataRequired()])
    falcon_four = StringField('F4', default=0, validators=[DataRequired()])
    falcon_sixteen = StringField('F16', default=0, validators=[DataRequired()])
    twentyfour_to_five = StringField('24v to 5v', default=0, validators=[DataRequired()])
    twentyfour_to_twelve = StringField('24v to 12v', default=0, validators=[DataRequired()])
    number_of_datas = StringField('Data', default=0, validators=[DataRequired()])
    raspberry_pi = StringField('Pies', default=0, validators=[DataRequired()])
    tp_link = StringField('TP-Link', default=0, validators=[DataRequired()])
    spokes = StringField('Spokes', default=0, validators=[DataRequired()])
    boxes = TextAreaField('Boxes', render_kw={'placeholder': 'Enter boxes used...'}, validators=[DataRequired()])
    phoenix_one_by_one = StringField('Phoenix 1x1', default=0, validators=[DataRequired()])
    phoenix_one_by_two = StringField('Phoenix 1x2', default=0, validators=[DataRequired()])
    phoenix_two_by_two = StringField('Phoenix 2x2', default=0, validators=[DataRequired()])
    controller_number = StringField('', default=0, validators=[DataRequired()])
    submit = SubmitField('Submit')
