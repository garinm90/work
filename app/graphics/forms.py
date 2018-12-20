from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField

class CreateGraphicsForm(FlaskForm):
    vinyl = IntegerField('Vinyl Sq Ft', default=0)
    vinyl_on_aluminum = IntegerField('Vinyl on Aluminum Sq Ft', default=0)
    laminate = IntegerField('Laminate Sq Ft', default=0)
    matte = IntegerField('Matte Sq Ft', default=0)
    heavy = IntegerField('Heavy Sq Ft', default=0)
    backlit = IntegerField('Blacklit Cost', default=0)
    file_location = TextAreaField('File Locations')
    notes = TextAreaField('Notes')
    submit = SubmitField('Submit')