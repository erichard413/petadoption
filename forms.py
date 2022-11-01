from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, IntegerField, RadioField, SelectField, ValidationError
from wtforms.validators import InputRequired, Optional, Email, DataRequired

class AddPetForm(FlaskForm):
    """Form for adding snacks."""

    name = StringField("Pet Name", validators=[InputRequired(message="Pet name must be provided")])
    species = SelectField("Species", choices=[("cat", "Cat"), ("dog", "Dog"), ("porcupine", "Porcupine")])
    photo_url = StringField("Photo URL")
    age = IntegerField("Age", validators=[DataRequired(message="Age must be a number")])
    notes = StringField("Notes")
    available = BooleanField('Is this pet available for adoption?')
