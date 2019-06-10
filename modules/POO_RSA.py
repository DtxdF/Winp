# -*- coding: UTF-8 -*-

import rsa

class invalidKeys(Exception): """
Cuando las llaves importadas son incorrectas
"""

class noKeyFound(Exception): """
Cuando no se detecta que esta almacenado una clave
"""

class main:

    def __init__(self):

        """
        :bitsize int: Tamaño en bits de las claves
        """

        self.keys = [] # Aquí se almacenaran las claves

    def generate(self, bitsize=2040):

        """
        Genera el par de llaves
        """

        self.pub_key, self.priv_key = rsa.newkeys(bitsize)
        return True

    def export(self):

        """
        Exportar la clave pública y privada
        """

        return [self.pub_key, self.priv_key]

    def export_PublicKey(self):

        """
        Exportar la clave pública
        """

        return self.pub_key

    def export_PrivateKey(self):

        """
        Exportar la clave privada
        """

        return self.priv_key

    def import_PublicKey(self, key):

        """
        Importar la clave pública
        """

        pub_key = str(key)

        try:

            if not (pub_key.index('PublicKey') == 0):

                raise invalidKeys('No corresponde con la especificación')

        except ValueError:

            raise invalidKeys('No se encontraron valores validos que argumenten la especificación')

        pub_key = pub_key.replace(' ','').replace('PublicKey(','').replace(')','').split(',')

        if not (len(pub_key) == 2):

            raise invalidKeys('Hay demasiados o muy pocos argumentos para que la especificación de la clave pública sea correcta')

        self.pub_key = rsa.PublicKey(int(pub_key[0]), int(pub_key[1]))

        return True

    def import_PrivateKey(self, key):

        """
        Importar la clave privada
        """

        priv_key = str(key)

        try:

            if not (priv_key.index('PrivateKey') == 0):

                raise invalidKeys('No corresponde con la especificación')

        except ValueError:

            raise invalidKeys('No se encontraron valores validos que argumenten la especificación')

        priv_key = priv_key.replace(' ','').replace('PrivateKey(','').replace(')','').split(',')

        if not (len(priv_key) == 5):

            raise invalidKeys('Hay demasiados o muy pocos argumentos para que la especificación de la clave privada sea correcta')

        self.priv_key = rsa.PrivateKey(int(priv_key[0]), int(priv_key[1]), int(priv_key[2]), int(priv_key[3]), int(priv_key[4]))

        return True

    def encrypt(self, data):

        try:

            return rsa.encrypt(data, self.pub_key)

        except AttributeError:

            raise noKeyFound('No se detecto la clave pública')

    def decrypt(self, data):

        try:

            return rsa.decrypt(data, self.priv_key)

        except AttributeError:

            raise noKeyFound('No se detecto la clave privada')

    def sign(self, data, hash_algo='SHA-512'):

        try:

            return rsa.sign(data, self.priv_key, hash_algo)

        except AttributeError:

            raise noKeyFound('No se detecto la clave privada')

    def verify(self, data, signature):

        try:

            return rsa.verify(data, signature, self.priv_key)

        except AttributeError:

            raise noKeyFound('No se detecto la clave privada')
