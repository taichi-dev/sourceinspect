from . import BaseInspector


def get_blender_text_name(file):
    import os
    if file.startswith(os.path.sep) and file.count(os.path.sep) == 1:
        return file[1:]      # untitled blender file, "/Text"

    i = file.rfind('.blend' + os.path.sep)
    if i != -1:
        return file[i + 7:]  # saved blender file, "hello.blend/Text"

    return None


def find_blender_source(object):
    import inspect

    old_getfile = inspect.getfile

    if not hasattr(inspect.getmodule(object), '__file__'):
        from . import CodeInspector
        proxy = CodeInspector(object)
        return {'_source': lambda: proxy.source,
                '_lineno': lambda: proxy.lineno,
                '_file': lambda: proxy.file}

    def new_getfile(object):
        import tempfile
        import atexit
        import bpy
        import os

        file = old_getfile(object)
        blender_text = get_blender_text_name(file)
        if blender_text is None:
            return file

        content = bpy.data.texts[blender_text].as_string()
        try:
            return new_getfile._si_cache[content]
        except KeyError:
            pass

        suffix = '_' + blender_text
        fd, name = tempfile.mkstemp(prefix='.SI_blender_', suffix=suffix)
        os.close(fd)
        with open(name, 'w') as f:
            f.write(content)

        atexit.register(os.unlink, name)
        new_getfile._si_cache[content] = name
        return name

    inspect.getfile = new_getfile
    new_getfile._si_cache = {}

    from . import DillInspector
    proxy = DillInspector(object)
    return {'_source': lambda: proxy.source,
            '_lineno': lambda: proxy.lineno,
            '_file': lambda: proxy.file}


class BlenderInspector(BaseInspector):
    def __init__(self, object):
        self.object = object
        self.__dict__.update(find_blender_source(self.object))
