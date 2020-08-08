from . import BasicInspector


class BuiltinInspector(BasicInspector):
    def __init__(self, object):
        self.object = object

        import inspect
        self.inspect = inspect
