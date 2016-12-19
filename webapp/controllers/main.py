#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint,flash,redirect,url_for,render_template,current_app
from flask import session
from flask_login import login_user,logout_user

from webapp.forms import LoginForm,RegisterForm
from webapp.models import User, db

from flask_principal import Identity,AnonymousIdentity,identity_changed


main_blueprint = Blueprint(
	'main',
	__name__,
	template_folder='../templates/main'
)

@main_blueprint.route('/')
def index():
	# return redirect(url_for('blog.home'))
	return render_template("show.html")


@main_blueprint.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()

	if form.validate_on_submit():

		# session['username'] = form.username.data
		user = User.query.filter_by(username=form.username.data).one()
		login_user(user,remember=form.remember.data)

		identity_changed.send(
			current_app._get_current_object(),
			identity=Identity(user.id)
		)

		flash("You have been logged in.",category='success')
		return redirect(url_for('blog.home'))

	return render_template('login.html',form=form)

@main_blueprint.route('/logout',methods=['GET','POST'])
def logout():
	# session.pop('username',None)
	logout_user()

	identity_changed.send(
		current_app._get_current_object(),
		identity = AnonymousIdentity()
	)

	flash("You are logged out.",category='success')
	return redirect(url_for('.login'))



@main_blueprint.route('/register',methods=['GET','POST'])
def register():
	form = RegisterForm()

	if form.validate_on_submit():
		new_user = User('')
		new_user.username = form.username.data
		new_user.set_password(form.password.data)

		db.session.add(new_user)
		db.session.commit()

		flash("Your user has been created, please login.",category='success')
		return redirect(url_for('.login'))

	return render_template('register.html',form=form)





































