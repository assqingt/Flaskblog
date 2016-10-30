#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import random
import time

from webapp import create_app
from webapp.models import db,User,Post, Tag

app = create_app('webapp.config.DevConfig')


user = User.query.get(1)
tag_one = Tag('Python')
tag_two = Tag('Flask')
tag_three = Tag('SQLAlchemy')
tag_four = Tag('Jinja')
tag_list = [tag_one,tag_two,tag_three,tag_four]

s = "Example text"

for i in range(100):
	new_post = Post("Post "+str(i))
	new_post.user = user
	new_post.publish_date = datetime.datetime.now()
	new_post.text = s
	new_post.tags = random.sample(tag_list,random.randint(1,3))
	db.session.add(new_post)
	time.sleep(0.1)

db.session.commit()

