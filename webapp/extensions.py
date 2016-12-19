#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_principal import Principal,Permission,RoleNeed
from flask_restful import Api
from flask_celery import Celery

bcrypt = Bcrypt()

login_manager = LoginManager()

login_manager.login_view = 'main.login'
login_manager.session_protection = 'strong'
login_manager.login_message = 'Please login to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(userid):
	from webapp.models import User
	return User.query.get(userid)

principals = Principal()

admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))


rest_api = Api()

celery = Celery()