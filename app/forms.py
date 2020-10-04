from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField, TextAreaField, \
    DateField, DateTimeField, TimeField, IntegerField, FileField
from wtforms.validators import DataRequired, NumberRange, Email, Length, EqualTo, Optional
# from flask_babel import lazy_gettext as _l
import pycountry
import datetime


class NewProjectForm(FlaskForm):
    title = StringField('Project title', validators=[DataRequired(), Length(max=100)],
                        render_kw={"class": "input-block input-title"})
    background_image = StringField('Background image', validators=[Length(max=200)],
                                   render_kw={"class": "input-block input-source"})
    github_url = StringField(validators=[Length(max=200)], render_kw={"class": "input-block input-source"})
    website_url = StringField(validators=[Length(max=200)], render_kw={"class": "input-block input-source"})
    description = TextAreaField("Content", validators=[DataRequired(), Length(max=5000)],
                                render_kw={"class": "input-block"})
    submit = SubmitField('Publish', render_kw={"class": "btn-submit"})


class UserForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Length(max=120)],
                        render_kw={"class": "input-block"})
    name = StringField(validators=[Length(max=64)],
                       render_kw={"class": "input-block"})
    surname = StringField(validators=[Length(max=64)], render_kw={"class": "input-block"})
    phone = StringField(validators=[Length(max=15)], render_kw={"class": "input-block"})
    gender = SelectField(choices=[('m', "Male"), ('f', "Female")])
    submit = SubmitField('Send', render_kw={"class": "btn-submit"})


class ContactForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Length(max=120)],
                        render_kw={"class": "input-block"})
    name = StringField(validators=[DataRequired(), Length(max=100)],
                       render_kw={"class": "input-block"})
    message_header = StringField(validators=[DataRequired(), Length(max=200)],
                                 render_kw={"class": "input-block input-title"})
    message_body = TextAreaField(validators=[DataRequired(), Length(max=5000)],
                                 render_kw={"class": "input-block"})
    submit = SubmitField('Send', render_kw={"class": "btn-submit"})
