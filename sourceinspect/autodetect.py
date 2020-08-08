def get_inspector():
    from . import IPythonInspector, RemoteInspector, BlenderInspector, DillInspector
    import sys

    try:
        get_ipython()
        return IPythonInspector
    except NameError:
        pass

    if 'idlelib' in sys.modules:  # IDLE use code.py in seperate process
        return RemoteInspector

    if 'bpy' in sys.modules:      # Blender use code.py in same process
        return BlenderInspector

    return DillInspector
