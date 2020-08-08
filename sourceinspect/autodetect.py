def get_inspector():
    from . import IPythonInspector, RemoteInspector, BlenderInspector, DillInspector
    import sys

    if hasattr(__builtins__, '__IPYTHON__'):
        return IPythonInspector
    if hasattr(__builtins__, 'get_ipython'):
        return IPythonInspector

    if 'idlelib' in sys.modules:  # IDLE use code.py in seperate process
        return RemoteInspector

    if 'bpy' in sys.modules:      # Blender use code.py in same process
        return BlenderInspector

    return DillInspector
