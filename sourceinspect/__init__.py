from .autodetect import get_getfile
import dill.source
import inspect


class InspectMock():
    def __enter__(self):
        self.getfile = get_getfile()
        if self.getfile is not None:
            inspect._si_old_getfile = inspect.getfile
            dill.source._si_old_getfile = dill.source.getfile
            inspect.getfile = self.getfile
            dill.source.getfile = self.getfile

        return self

    def __exit__(self, *_):
        if self.getfile is not None:
            inspect.getfile = inspect._si_old_getfile
            dill.source.getfile = dill.source._si_old_getfile
            del inspect._si_old_getfile
            del dill.source._si_old_getfile


def getsource(object):
    with InspectMock():
        return dill.source.getsource(object)

def getsourcelines(object):
    with InspectMock():
        return dill.source.getsourcelines(object)

def getsourcefile(object):
    with InspectMock():
        return dill.source.getsourcefile(object)


__all__ = [
    'getsource',
    'getsourcelines',
    'getsourcefile',
]
