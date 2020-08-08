from . import BasicInspector


class IPythonInspector(BasicInspector):
    def __init__(self, object):
        self.object = object

        import IPython
        self.inspect = IPython.core.oinspect

    def _lineno(self):
        return self.inspect.find_source_lines(self.object)

    def _file(self):
        lineno = self.getlineno()
        return f'<IPython:{lineno}>'
