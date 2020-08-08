class BaseInspector:
    def __init__(self, object):
        self.object = object

    @property
    def source(self):
        raise NotImplementedError

    @property
    def lineno(self):
        raise NotImplementedError

    @property
    def file(self):
        raise NotImplementedError

    @classmethod
    def getsource(Inspect, object):
        ins = Inspect(object)
        return ins.source

    @classmethod
    def getsourcefile(Inspect, object):
        ins = Inspect(object)
        return ins.file

    @classmethod
    def getsourcelines(Inspect, object):
        ins = Inspect(object)
        lines = [_ + '\n' for _ in ins.source.split('\n')]
        return lines, ins.lineno


class BasicInspector(BaseInspector):
    def __init__(self, object, inspect):
        self.object = object
        self.inspect = inspect

    def getsource(self):
        return self.inspect.getsource(self.object)

    def getlineno(self):
        return self.inspect.getsourcelines(self.object)[1]

    def getfile(self):
        return self.inspect.getsourcefile(self.object)

    @property
    def source(self):
        ret = self.getsource()
        self.__dict__['source'] = ret
        return ret

    @property
    def lineno(self):
        ret = self.getlineno()
        self.__dict__['lineno'] = ret
        return ret

    @property
    def file(self):
        ret = self.getfile()
        self.__dict__['file'] = ret
        return ret


from .builtin import BuiltinInspector
from .ipython import IPythonInspector
from .dill import DillInspector
from .code import CodeInspector
from .autodetect import get_inspector


__all__ = [
    'BuiltinInspector',
    'IPythonInspector',
    'DillInspector',
    'CodeInspector',
    'get_inspector',
]
