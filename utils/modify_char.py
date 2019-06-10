# -*- coding: UTF-8 -*-

from utils import config
from platform import system

def modify(string):

	if (system() == 'Windows'):

		for key, value in config.conf['custom_chars'].items():
		
			string = string.replace(key, value)

	return string