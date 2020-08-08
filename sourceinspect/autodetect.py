from . import *


def get_inspector():
    if hasattr(__builtins__, '__IPYTHON__'):
        return IPythonInspector
    if hasattr(__builtins__, 'get_ipython'):
        return IPythonInspector

    return DillInspector
