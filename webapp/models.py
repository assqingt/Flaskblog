#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from webapp.extensions import bcrypt
from flask_login import AnonymousUserMixin
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,SignatureExpired,BadSignature



db = SQLAlchemy()

tags = db.Table('post_tags', db.Column('post_id', db.Integer(), db.ForeignKey('post.id')),
	db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id')))

roles = db.Table('role_users',db.Column('user_id',db.Integer(),db.ForeignKey('user.id')),
                 db.Column('role_id',db.Integer(),db.ForeignKey('role.id')))


class User(db.Model):
	# __tablename__ = "blog_user"

	id = db.Column(db.Integer(), primary_key=True)
	username = db.Column(db.String(255))
	password = db.Column(db.String(255))

	posts = db.relationship('Post', backref='user', lazy='dynamic')

	roles = db.relationship('Role', secondary=roles,backref = db.backref('users',lazy='dynamic'))

	def __init__(self, username):
		self.username = username

	def __repr__(self):
		return "<User '{}'>".format(self.username)

	def set_password(self,password):
		self.password = bcrypt.generate_password_hash(password)

	def check_password(self,password):
		return bcrypt.check_password_hash(self.password,password)

	def is_authenticated(self):
		if isinstance(self,AnonymousUserMixin):
			return False
		else:
			return True

	def is_active(self):
		return True

	def id_anonymous(self):
		if isinstance(self,AnonymousUserMixin):
			return True
		else:
			return False

	def get_id(self):
		return self.id

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(
			current_app.config['SECRET_KEY']
		)

		try:
			data = s.loads(token)
		except SignatureExpired:
			return None
		except BadSignature:
			return None
		user =User.query.get(data['id'])
		return user

class Post(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	title = db.Column(db.String(255))
	text = db.Column(db.Text())
	publish_date = db.Column(db.DateTime())
	user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

	comments = db.relationship('Comment', backref='post', lazy='dynamic')

	tags = db.relationship('Tag', secondary=tags, backref=db.backref('posts', lazy='dynamic'))

	def __init__(self, title):
		self.title = title

	def __repr__(self):
		return "<Post '{}'>".format(self.title)


class Comment(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(255))
	text = db.Column(db.Text())
	date = db.Column(db.DateTime())
	post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))


class Tag(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	title = db.Column(db.String(255))

	def __init__(self, title):
		self.title = title

	def __repr__(self):
		return "<Tag '{}'>".format(self.title)


class Role(db.Model):
	id = db.Column(db.Integer(),primary_key=True)
	name = db.Column(db.String(80),unique=True)
	description = db.Column(db.String(255))

	def __init__(self,name):
		self.name = name

	def __repr__(self):
		return "<Role {}>".format(self.name)





























