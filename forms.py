from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, SelectField, PasswordField
from wtforms.fields.html5 import DateField, TimeField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset your password')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')


class TextArea(FlaskForm):
    title = TextAreaField('Put your title', render_kw={'rows': 20}, validators=[DataRequired()])
    text = TextAreaField('Put your text right there', validators=[DataRequired()])
    submit = SubmitField('Create your article')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')


class NotificationForm(FlaskForm):
    note = TextAreaField('Write your notification here', render_kw={'rows': 20}, validators=[DataRequired()])
    # date = DateField('Enter Date', format='%Y-%m-%d')
    # time = TimeField('Enter time', format='%H:%M')20
    datetime = DateTimeField('Set date', format='%Y-%m-%d %H:%M')
    submit = SubmitField('Create Notification')


class SignUpForm(FlaskForm):
    nickname = StringField('Nickname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    repassword = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    country = SelectField('Country')
    submit = SubmitField('Sign Up')
