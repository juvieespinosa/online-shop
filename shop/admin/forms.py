from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, validators, IntegerField, \
    FileField, FloatField
from wtforms.validators import DataRequired, URL, Length, Email, EqualTo, ValidationError
from .models import User


class RegistrationForm(FlaskForm):
	name = StringField("Name:", validators=[DataRequired(), Length(max=80)])
	email = StringField("Email:", validators=[DataRequired(), Email()])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords must match')
	])
	confirm = PasswordField('Repeat Password')
	submit = SubmitField("Register")

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")