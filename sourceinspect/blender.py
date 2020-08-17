import tempfile
import inspect
import atexit
import os

def get_blender_text_name(file):
    import os
    if file.startswith(os.path.sep) and file.count(os.path.sep) == 1:
        return file[1:]      # untitled blender file, "/Text"

    i = file.rfind('.blend' + os.path.sep)
    if i != -1:
        return file[i + 7:]  # saved blender file, "hello.blend/Text"

    return None



def blender_getfile(object):
    import bpy

    file = inspect._si_old_getfile(object)
    blender_text = get_blender_text_name(file)
    if blender_text is None:
        return file

    content = bpy.data.texts[blender_text].as_string()

    try:
        return blender_getfile._si_cache[content]
    except KeyError:
        pass

    suffix = '_' + blender_text + '.py'
    fd, name = tempfile.mkstemp(prefix='SI_Blender_', suffix=suffix)
    os.close(fd)
    with open(name, 'w') as f:
        f.write(content)

    atexit.register(os.unlink, name)
    blender_getfile._si_cache[content] = name
    return name

blender_getfile._si_cache = {}
