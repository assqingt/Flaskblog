#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager,Server

from webapp import create_app
from webapp.models import db,User,Tag,Comment,Post,Role

env = os.environ.get('WEBAPP_ENV','dev')
app = create_app('webapp.config.%sConfig' % env.capitalize())

manager = Manager(app)
migrate = Migrate(app,db)

manager.add_command('server',Server())
manager.add_command('db',MigrateCommand)

@manager.shell
def make_shell_context():
	return {
		'app':app,
		'db':db,
		'User':User,
		'Post':Post,
		'Comment':Comment,
		'Tag':Tag,
		'Role':Role
	}

if __name__ == '__main__':
	manager.run()