#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, TextAreaField,PasswordField,BooleanField
from wtforms.validators import DataRequired, Length,EqualTo,URL
from webapp.models import User


class CommentForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired(), Length(max=255)])
	text = TextAreaField('Comment', validators=[DataRequired()])


# 自定义邮件验证
def custom_email(form, field):
	if not re.match(r'[^@]+@[^@]+\.[^@]+', field.data):
		raise ValidationError('Field must be a valid email address.')


class LoginForm(FlaskForm):
	username = StringField('Username',[DataRequired(),Length(max=255)])
	password = PasswordField('Password',[DataRequired()])
	remember = BooleanField('Remember Me')


	def validate_on_submit(self):
		check_validate = super(LoginForm, self).validate_on_submit()

		if not check_validate:
			return False

		user = User.query.filter_by(username=self.username.data).first()

		if not user:
			self.username.errors.append(
				'Invalid username or password'
			)
			return False

		if not user.check_password(self.password.data):
			self.username.errors.append(
				'Invalid username or password'
			)
			return False

		return True


class RegisterForm(FlaskForm):
	username = StringField('Username',[DataRequired(),Length(max=255)])
	password = PasswordField('Password',[DataRequired(),Length(min=8)])
	confirm = PasswordField('Confirm Password',[DataRequired(),EqualTo('password')])

	def validate_on_submit(self):
		check_validate = super(RegisterForm, self).validate_on_submit()

		if not check_validate:
			return False

		user = User.query.filter_by(username=self.username.data).first()

		if user:
			self.username.errors.append(
				'User with that name already exists'
			)
			return False

		return True



class PostForm(FlaskForm):
	title = StringField('Title',[DataRequired(),Length(max=255)])
	text = TextAreaField('Content',[DataRequired()])































