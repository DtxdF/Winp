# -*- coding: UTF-8 -*-

import sys
from utils import _input

def invoke_quit():

    quit_quest = _input._input("¿Desea salir realmente? - [1 o 0]: ")

    if (quit_quest):

        if (quit_quest[0].lower() == '1'):

            print("Saliendo ...")
            sys.exit(0)
