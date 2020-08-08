from . import BasicInspector


class DillInspector(BasicInspector):
    def __init__(self, object):
        self.object = object

        import dill.source
        self.inspect = dill.source

    def getlineno(self):
        return self.inspect.getsourcelines(self.object)[1] + 1
