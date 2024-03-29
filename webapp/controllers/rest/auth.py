#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import abort,current_app
from flask_restful import Resource
from .parsers import user_post_parser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from webapp.models import User


class AuthApi(Resource):
	def post(self):
		args = user_post_parser.parse_args()
		user = User.query.filter_by(username=args['username']).one()

		if user.check_password(args['password']):
			s = Serializer(
				current_app.config['SECRET_KEY'],
				expires_in=600
			)
			return {"token":str(s.dumps({'id':user.id})).strip('b\'')}
		else:
			abort(401)