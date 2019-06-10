# -*- coding: UTF-8 -*-

import socks
import socket

socket_reverse = socket.socket

class invalidAddress(Exception): """
    Excepción generada cuando se introduce una dirección IP
    Invalida.
"""

class invalidPort(Exception): """
    Excepción generada cuando se introduce un puerto Inval_
    ido.
"""

def transfor(proxy_type=socks.PROXY_TYPE_SOCKS4, proxy_addr="127.0.0.1:9050", rdns=True, username=None, password=None):
    
    """Establece una conexión con el proxy y cambia el tipp de socket estandar

    proxy_type "El tipo de proxy. use socks.PROXY_TYPES, para todos los tipos de proxys"
    proxy_addr "La dirección del proxy"
    rdns "Permite usar dns remoto"
    username "El nombre de usuario del proxy (Si lo requiere)
    password "La contraseña del proxy (Si lo requiere)
    """
    if (proxy_addr.count(":") <> 1):

        raise invalidAddress("Dirección invalida.")

    proxy_addr_tuple = proxy_addr.split(":")

    try:

        proxy_addr_tuple[1] = int(proxy_addr_tuple[1])

    except ValueError:

        raise invalidPort("Puerto invalido.")

    socks.setdefaultproxy(proxy_type, proxy_addr_tuple[0], proxy_addr_tuple[1], rdns=rdns, username=username, password=password)

    socket.socket = socks.socksocket

    return True

def restruct():

    "Restructura o vuelve al socket sin conexión con el proxy"

    global socket_reverse

    socket.socket = socket_reverse

    return True
