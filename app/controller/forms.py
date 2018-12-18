from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

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
