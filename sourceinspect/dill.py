from . import BasicInspector


class DillInspector(BasicInspector):
    def __init__(self, object):
        self.object = object

        try:
            import dill.source
            self.inspect = dill.source
        except ImportError:
            import inspect
            self.inspect = inspect

    def _lineno(self):
        return self.inspect.getsourcelines(self.object)[1] + 1
