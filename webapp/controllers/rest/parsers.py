#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_restful import reqparse

post_get_parser = reqparse.RequestParser()
post_get_parser.add_argument(
	'page',
	type=int,
	location=['json','args','headers'],
	required = False
)

post_get_parser.add_argument(
	'user',
	type=str,
	location=['json','args','headers']
)


post_post_parser = reqparse.RequestParser()
post_post_parser.add_argument(
	'title',
	type=str,
	required=True,
	help='title is required'
)
post_post_parser.add_argument(
	'text',
	type=str,
	required=True,
	help='body text is required'
)
post_post_parser.add_argument(
	'tags',
	type=str,
	action='append'
)
post_post_parser.add_argument(
	'token',
	type=str,
	required=True,
	help='Auth token is required to create posts'
)




user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument(
	'username',
	type=str,
	required=True
)
user_post_parser.add_argument(
	'password',
	type=str,
	required=True
)


post_put_parser = reqparse.RequestParser()
post_put_parser.add_argument(
	'token',
	type=str,
	required=True,
	help='Auth token is required to edit post'
)
post_put_parser.add_argument(
	'title',
	type=str
)
post_put_parser.add_argument(
	'text',
	type=str
)
post_put_parser.add_argument(
	'tags',
	type=str,
	action='append'
)


post_delete_parser = reqparse.RequestParser()
post_delete_parser.add_argument('token',type=str,required=True,help='Auth token is required to delete post')