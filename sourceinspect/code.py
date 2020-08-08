from . import BasicInspector


source_lines = []


def hack(code):
    import functools
    old_runsource = code.InteractiveInterpreter.runsource

    @functools.wraps(old_runsource)
    def new_runsource(self, source, *args, **kwargs):
        source_lines.append(source)
        return old_runsource(self, source, *args, **kwargs)

    code.InteractiveInterpreter.runsource = new_runsource



class CodeInspector(BasicInspector):
    def __init__(self, object):
        self.object = object

        import dill.source
        self.inspect = dill.source

    def _source(self):
        return 1


hack(__import__('code'))
