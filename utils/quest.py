# -*- coding: UTF-8 -*-

def quest(raw_input_string, value_true, value_false, value_len=1):

    debug = raw_input("%s - [%s o %s]: " % (str(raw_input_string), str(value_true)[:value_len], str(value_false)[:value_len]))

    if (debug[:value_len].lower() == str(value_true).lower()):

        return True

    else:

        return False
