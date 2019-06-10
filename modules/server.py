# -*- coding: UTF-8 -*-

import socket
import uuid
import shelve
from time import sleep
from utils import is_value_in_array
from utils import config
from modules import hashing
from threading import Thread
from os.path import isfile, basename
from utils import hibrid
from utils import client_interact

clients = []
clients_to_socket = {}
clients_for_interact = []
server_obj = None

class Server(Thread):

    def __init__(self, server_obj, client_obj, client_addr, buff, keys):

        Thread.__init__(self)
	self.client_obj = client_obj
        self.client_addr = client_addr
        self.buff = buff
        self.keys = keys

    def run(self):

	global clients_for_interact, clients, clients_to_socket

	execute = True
	verify_username = False
	verify_password = False

	credentials = config.conf['credentials']
	username_list = credentials['username']
	password_list = credentials['password']
       
	remote_credentials = hibrid.decrypt(client_interact.recv(self.client_obj), self.keys[1])

        if (type(remote_credentials) == bool):

            return False

        if (remote_credentials.count(';') == 1):

	    remote_username, remote_password = remote_credentials.split(';')

	    for index in username_list:

	        if (hashing.hash(index, hash_algo='double') == remote_username):

	            verify_username = True

	            break

	    for index in password_list:

	        if (hashing.hash(index, hash_algo='double') == remote_password):

	            verify_password = True

	            break

	    if (verify_username == False) or (verify_password == False):

	        execute = False

	        self.client_obj.send('0')

	    else:

	        client_addr = "%sP%d" % (str(self.client_addr[0]), int(self.client_addr[1]))

	        if not (is_value_in_array.is_value_in_array(clients, client_addr)):

	            clients.append(client_addr)
	            clients_to_socket[client_addr] = self.client_obj

                self.client_obj.send('1')

        else:

            execute = False

            self.client_obj.send('0')

        while(execute):

            try:

                real_data = hibrid.decrypt(client_interact.recv(self.client_obj), self.keys[1])

            except Exception as Except:

                break

            if (type(real_data) == bool):

                break

            if (real_data[:9].lower() == 'download/'):
                
                name = basename(real_data[9:].replace(real_data[9:].split()[0]+' ', ''))

                with open(name, 'wb') as write_file:

                    write_file.write(real_data[9:].split()[0].decode("hex"))

                print('"%s" se decargo satisfactoriamente!' % (name))


            else:

	        address, rport = self.client_addr 
	        clients_for_interact.append({"%sP%d-id:%s" % (str(address), int(rport), hashing.hash(str(uuid.uuid4()), hash_algo='md5')):{'socket':self.client_obj, 'data':real_data, 'length':len(real_data)}})

def run_server(lhost='0.0.0.0', lport=7476, limit=0, family=socket.AF_INET, protocol=socket.SOCK_STREAM, buff=1024):

    global server_obj

    server_obj = socket.socket(family, protocol)
    server_obj.bind((lhost, lport))
    server_obj.listen(limit)

    while True:

        if (isfile(config.conf['shelve_setting'])):

            try:

                keys = shelve.open(config.conf['shelve_setting'])['keys']

            except KeyError:

                sleep(config.conf['time_setting']['sleep'])
                continue

            client_obj, client_addr = server_obj.accept() 

            server_thread = Server(server_obj, client_obj, client_addr, buff, keys)
            server_thread.start()

        else:

            sleep(config.conf['time_setting']['sleep'])
