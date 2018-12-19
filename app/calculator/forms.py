from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField

class PowerCalculatorForm(FlaskForm):
    nine_led_puck = IntegerField('Puck 9', default=0)
    six_led_puck = IntegerField('Puck 6', default=0)
    submit = SubmitField('Calculate')
