# -*- coding: UTF-8 -*-

from Crypto.Cipher import AES
from Crypto import Random
from hashlib import md5

class AESCript:

    def __init__(self, password, mode=AES.MODE_CBC):

        self.password = md5(password).digest()
        self.block_size = 32
        self.mode = mode

    def pad(self, string):

        return string + (self.block_size - len(string) % self.block_size) * chr(self.block_size - len(string) % self.block_size)

    def unpad(self, string):

        return string[:-ord(string[len(string)-1:])]

    def encrypt(self, raw):

        iv = Random.new().read(AES.block_size)
        method = AES.new(self.password, self.mode, iv)

        return iv + method.encrypt(self.pad(raw))

    def decrypt(self, encrypted_data):

        iv = encrypted_data[:AES.block_size]
        method = AES.new(self.password, self.mode, iv)

        return self.unpad(method.decrypt(encrypted_data)[AES.block_size:])
