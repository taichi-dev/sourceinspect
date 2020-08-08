from . import *


def get_inspector():
    if hasattr(__builtins__, '__IPYTHON__'):
        return IPythonInspector
    if hasattr(__builtins__, 'get_ipython'):
        return IPythonInspector

    import sys
    if 'idlelib' in sys.modules:  # IDLE use code.py in seperate process
        return RemoteInspector

    if 'bpy' in sys.modules:      # Blender use code.py in same process
        return CodeInspector

    return DillInspector
