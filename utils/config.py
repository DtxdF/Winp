# -*- coding: UTF-8 -*-

import socks
import socket
from terminaltables import AsciiTable, DoubleTable, GithubFlavoredMarkdownTable, PorcelainTable, SingleTable

conf = {
        'proxy_setting':{
            'use':False,
            'proxy_type':socks.PROXY_TYPE_SOCKS4, 
            'proxy_addr':'127.0.0.1:9050',
            'rdns':True,
            'username':None,
            'password':None
            },
        'rsa_setting':{
            'bitsize':1024,
            },
        'socket_setting':{
            'lhost':'127.0.0.1',
            'lport':8043,
            'family':socket.AF_INET,
            'protocol':socket.SOCK_STREAM,
            'limit':0,
            'buffer_limit':1024
            },
        'credentials':{
            'username':['root'],
            'password':['password123!']
            },
        'style':{
            'input_string':'Winp> ',
            'table_style':SingleTable
            },
        'time_setting':{
            'sleep':1
            },
        'keys_setting':{
            'bitsize':1024
            },
        'shelve_setting':'db.dat',
	    'custom_chars':{
		'ñ':'\xa4',
		'ó':'\xa2',
		'í':'\xa1',
		'ú':'\xa3',
		'á':'\xa0'
	    }
        }
