#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webapp.extensions import celery



@celery.task
def add(x,y):
	return x+y