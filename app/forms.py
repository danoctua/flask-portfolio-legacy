from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField, TextAreaField, \
    DateField, DateTimeField, TimeField, IntegerField, FileField
from wtforms.validators import DataRequired, NumberRange, Email, Length, EqualTo, Optional
# from flask_babel import lazy_gettext as _l
import pycountry
import datetime


class NewProjectForm(FlaskForm):
    title = StringField('Project title', validators=[DataRequired()], render_kw={"class": "input-block input-title"})
    background_image = StringField('Background image', validators=[], render_kw={"class": "input-block input-source"})
    description = TextAreaField("Content", validators=[DataRequired(), Length(max=5000)], render_kw={"class": "input-block"})
    submit = SubmitField('Publish', render_kw={"class": "btn-submit"})
