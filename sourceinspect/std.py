from . import BasicInspector


class StdInspector(BasicInspector):
    def __init__(self, object):
        self.object = object

        import inspect
        self.inspect = inspect
