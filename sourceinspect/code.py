from . import BasicInspector


source_lines = []


def hack(code):
    import functools
    old_runsource = code.InteractiveInterpreter.runsource

    @functools.wraps(old_runsource)
    def new_runsource(self, source, *args, **kwargs):
        source_lines.append(source)
        return old_runsource(self, source, *args, **kwargs)

    new_runsource._is_code_hook = 1
    code.InteractiveInterpreter.runsource = new_runsource


def find_interactive_source(object, lines=source_lines):
    for x in lines:
        x = x.strip()
        i = x.find('def ')
        if i == -1:
            continue
        name = x[i + 4:]
        name = name.split(':', maxsplit=1)[0]
        name = name.split('(', maxsplit=1)[0]
        name = name.strip()
        if name == object.__name__:
            return x

    from . import DillInspector
    return DillInspector.getsource(object)

    #raise NameError(
    #        f'Could not find source for object "{object.__name__}"!\n'
    #        'Currently `sourceinspect` is only able to inspect source'
    #        'of functions in interactive shells yet, sorry!')


class CodeInspector(BasicInspector):
    def __init__(self, object):
        self.object = object

        import dill.source
        self.inspect = dill.source

    def _source(self):
        return find_interactive_source(self.object)


hack(__import__('code'))
