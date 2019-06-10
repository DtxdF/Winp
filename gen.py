# -*- coding: UTF-8 -*-

from modules import server
from utils import main
from utils import config
from utils import is_value_in_array
from os.path import isdir
from time import sleep
import threading

# Configuración global

configuration = config.conf

# Configuración de RSA

rsa_settings = configuration['rsa_setting']
rsa_bitsize = rsa_settings['bitsize']

# Configuración del servidor

socket_settings = configuration['socket_setting']
socket_lhost = socket_settings['lhost']
socket_lport = socket_settings['lport']
socket_family = socket_settings['family']
socket_protocol = socket_settings['protocol']
socket_buffer_limit = socket_settings['buffer_limit']
socket_limit = socket_settings['limit']

# Configuración del tiempo

time_settings = configuration['time_setting']
time_sleep = time_settings['sleep']

# Configuración de estilos

style_settings = configuration['style']
style_input_string = style_settings['input_string']

server_thread = threading.Thread(target=server.run_server, name='Server', args=(socket_lhost, socket_lport, socket_limit, socket_family, socket_protocol, socket_buffer_limit))
server_thread.setDaemon(True)
server_thread.start()

# Si se usa como api se necesitara información

clients = []
clients_for_interact = []
clients_to_socket = {}
server_obj = None

# Menu

control = main.main()

# Detección de clientes

def client_detection():

    global control, server, time_sleep, clients, clients_for_interact, clients_to_socket, server_obj

    while True:

        control.clients = server.clients
        control.clients_for_interact = server.clients_for_interact
        control.clients_to_socket = server.clients_to_socket
        control.server_obj = server.server_obj

        # Definimos las variables de el script principal

        clients = server.clients
        clients_for_interact = server.clients_for_interact
        clients_to_socket = server.clients_to_socket
        server_obj = server.server_obj

        sleep(time_sleep)

client_detection_thread = threading.Thread(target=client_detection, name="Client_Detection")
client_detection_thread.setDaemon(True)
client_detection_thread.start()

# Ejecutamos la entrada de datos

control.config = configuration

if __name__ == '__main__':

    control.entry_mode_init()
