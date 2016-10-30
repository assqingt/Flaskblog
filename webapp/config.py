#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path,getcwd


class Config(object):
	pass

class ProdConfig(Config):
	pass

class DevConfig(Config):
	DEBUG = True
	#SQLlite URI
	# SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
	# SQLALCHEMY_DATABASE_URI = 'sqlite:///D:\\PyPro\\note\\database.db'.replace('\\','/')
	SQLALCHEMY_DATABASE_URI = ('sqlite:///'+path.join(
		path.pardir,
		'database.db'
	)).replace('\\','/')
	#输出查询语句
	SQLALCHEMY_ECHO = False
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SECRET_KEY = 'IGnO2jMFwndZUtPm5WyG7pFzzP6YHoa1'

#
# print(('sqlite://'+path.dirname(getcwd())+'\database.db').replace('\\','/'))
# print(path.join(path.pardir,'database.db').replace('\\','/'))