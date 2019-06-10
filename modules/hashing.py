# -*- coding: UTF-8 -*-

from hashlib import md5, sha512

def hash(data, hash_algo='double'):

    if (hash_algo == 'double'):

        return md5(sha512(data).hexdigest()).hexdigest()

    elif (hash_algo == 'md5'):

        return md5(data).hexdigest()

    elif (hash_algo == 'sha512'):

        return sha512(data).hexdigest()

    else:

        return False

