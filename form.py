from flask_wtf import FlaskForm 
from wtforms import TextField, PasswordField, SubmitField, IntegerField, RadioField,TextAreaField


class blog_post(FlaskForm):
	title = TextField('Title: ')
	post = TextAreaField('Content: ')
	author = TextField('Writer Name: ')



	



