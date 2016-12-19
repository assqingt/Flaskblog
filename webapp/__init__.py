#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask,redirect,url_for

from webapp.config import DevConfig
from webapp.models import db
from webapp.controllers.blog import blog_blueprint
from webapp.extensions import bcrypt,login_manager,principals,rest_api,celery
from webapp.controllers.main import main_blueprint
from flask_principal import identity_loaded,UserNeed,RoleNeed
from flask_login import current_user
from webapp.controllers.rest.post import PostApi
from webapp.controllers.rest.auth import AuthApi



def create_app(object_name):
	app = Flask(__name__)
	app.config.from_object(object_name)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	principals.init_app(app)
	celery.init_app(app)



	rest_api.add_resource(PostApi,
	                      '/api/post',
	                      '/api/post/<int:post_id>',
	                      endpoint='api'
	                      )
	rest_api.add_resource(AuthApi,
	                      '/api/auth')
	rest_api.init_app(app)

	@identity_loaded.connect_via(app)
	def on_identity_loaded(sender,identity):
		#set the identity user object
		identity.user = current_user

		#add the user need to the identity
		if hasattr(current_user,'id'):
			identity.provides.add(UserNeed(current_user.id))

		#add each role to the identity
		if hasattr(current_user,'roles'):
			for role in current_user.roles:
				identity.provides.add(RoleNeed(role.name))


	# @app.route('/')
	# def index():
	# 	return redirect(url_for('blog.home'))


	app.register_blueprint(blog_blueprint)
	app.register_blueprint(main_blueprint)


	return app
if __name__ == '__main__':
	app = create_app(DevConfig)
	app.run()
