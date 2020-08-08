from . import BaseInspector


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

        ret = old_getfile(object)
        is_blender = ret.startswith('/') and ret.count('/') == 1
        if not is_blender:
            return ret

        content = bpy.data.texts[ret[1:]].as_string()
        try:
            return new_getfile._si_cache[content]
        except KeyError:
            pass

        fd, name = tempfile.mkstemp(prefix='SI_Blender_')
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
