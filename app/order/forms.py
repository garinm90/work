from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField, StringField, widgets
from wtforms.validators import NumberRange

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
