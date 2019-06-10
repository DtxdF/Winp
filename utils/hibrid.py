# -*- coding: UTF-8 -*-

from modules import POO_RSA as rsa
from modules import aes
from hashlib import md5
from uuid import uuid4
from json import loads, dumps

code = "hex"

def encode(string):

    global code

    return string.encode(code).strip()

def decode(string):

    global code

    return string.decode(code)

def encrypt(raw, public_key):
    
    if (raw == None):

        return False

    rsa_test = rsa.main()
    rsa_test.import_PublicKey(public_key)

    key_session = str(uuid4())

    aes_test = aes.AESCript(key_session)

    key_session = rsa_test.encrypt(key_session)

    content = {}

    content['key_session'] = encode(key_session)
    content['content'] = encode(aes_test.encrypt(raw))

    return encode(dumps(content))

def decrypt(enc_data, private_key):

    if (enc_data == None):

        return False

    enc_data = loads(decode(enc_data))

    rsa_test = rsa.main()
    rsa_test.import_PrivateKey(private_key)

    key_session = rsa_test.decrypt(decode(enc_data['key_session']))
    
    aes_test = aes.AESCript(key_session)

    content = aes_test.decrypt(decode(enc_data['content']))

    return content
