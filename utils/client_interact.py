# -*- coding: UTF-8 -*-

from utils import hibrid
from time import sleep

def send(client_object, pub_key, data):

    data = hibrid.encrypt(data, pub_key)
    data_lon = str(len(data))

    client_object.send(data_lon)
    sleep(1)
    client_object.send(data)

def recv(client_obj, buff=1024):

    try:
    
        data = ''
        maxbuffer = int(client_obj.recv(buff))

        while True:

	    data += str(client_obj.recv(buff))
            maxdata = len(data)

	    if (maxbuffer == maxdata):

	        return data

    except Exception as Except:

        print("Hubo un error con un socket ...")
