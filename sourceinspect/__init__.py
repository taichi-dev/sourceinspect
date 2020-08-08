class BaseInspector:
    def __init__(self, object):
        self.object = object

    def _source(self):
        raise NotImplementedError

    def _lineno(self):
        return 3

    def _file(self):
        return '<module>'

    @property
    def source(self):
        ret = self._source()
        self.__dict__['source'] = ret
        return ret

    @property
    def lineno(self):
        ret = self._lineno()
        self.__dict__['lineno'] = ret
        return ret

    @property
    def file(self):
        ret = self._file()
        self.__dict__['file'] = ret
        return ret

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

    def _source(self):
        return self.inspect.getsource(self.object)

    def _lineno(self):
        return self.inspect.getsourcelines(self.object)[1]

    def _file(self):
        return self.inspect.getsourcefile(self.object)


from .builtin import BuiltinInspector
from .ipython import IPythonInspector
from .remote import RemoteInspector
from .code import CodeInspector
from .dill import DillInspector
from .autodetect import get_inspector


def getsource(object):
    return get_inspector().getsource(object)

def getsourcelines(object):
    return get_inspector().getsourcelines(object)

def getsourcefile(object):
    return get_inspector().getsourcefile(object)


__all__ = [
    'getsource',
    'getsourcelines',
    'getsourcefile',
    'BuiltinInspector',
    'IPythonInspector',
    'RemoteInspector',
    'CodeInspector',
    'DillInspector',
    'get_inspector',
]
