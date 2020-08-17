import sys
import inspect

def get_getfile():
    if 'idlelib' in sys.modules:  # IDLE use code.py in seperate process
        from .remote import remote_getfile
        return remote_getfile

    if 'bpy' in sys.modules:      # Blender use code.py in same process
        from .blender import blender_getfile
        return blender_getfile

    return None
