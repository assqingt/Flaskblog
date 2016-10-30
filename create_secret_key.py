#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string

def random_string(randomlength=32):
	a=list(string.ascii_letters+string.digits)
	recret_key = ''
	for c in range(randomlength):
		recret_key += random.choice(a)
	return recret_key


if __name__ == '__main__':
	secret_key = random_string()
	print(secret_key)