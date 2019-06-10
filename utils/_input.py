# -*- coding: UTF-8 -*-

def _input(string):

    try:

        entrada = raw_input

    except NameError:

        entrada = input

    return entrada(string)

