from . import BasicInspector


class IPythonInspector(BasicInspector):
    def __init__(self, object):
        self.object = object

        import IPython
        self.inspect = IPython.core.oinspect

    def getlineno(self):
        return self.inspect.find_source_lines(self.object)

    def getfile(self):
        lineno = self.getlineno()
        return f'<IPython:{lineno}>'
