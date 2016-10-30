#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask,redirect,url_for

from webapp.config import DevConfig
from webapp.models import db
from webapp.controllers.blog import blog_blueprint
from webapp.extensions import bcrypt,login_manager
from webapp.controllers.main import main_blueprint

def create_app(object_name):
	app = Flask(__name__)
	app.config.from_object(object_name)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	# @app.route('/')
	# def index():
	# 	return redirect(url_for('blog.home'))


	app.register_blueprint(blog_blueprint)
	app.register_blueprint(main_blueprint)


	return app
if __name__ == '__main__':
	app = create_app(DevConfig)
	app.run()
