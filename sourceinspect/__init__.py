import inspect
import sys


def our_getfile(object):
    from .remote import remote_getfile
    return remote_getfile(object)


class InspectMock():
    def __enter__(self):
        inspect._si_old_getfile = inspect.getfile
        inspect.getfile = our_getfile
        return self

    def __exit__(self, *_):
        inspect.getfile = inspect._si_old_getfile
        del inspect._si_old_getfile


def getfile(object):
    with InspectMock():
        return inspect.getfile(object)

def findsource(object):
    with InspectMock():
        return inspect.findsource(object)

def getsource(object):
    with InspectMock():
        return inspect.getsource(object)

def getcomments(object):
    with InspectMock():
        return inspect.getcomments(object)

def getsourcelines(object):
    with InspectMock():
        return inspect.getsourcelines(object)

def getsourcefile(object):
    with InspectMock():
        return inspect.getsourcefile(object)


__all__ = [
    'InspectMock',
    'getfile',
    'findsource',
    'getsource',
    'getcomments',
    'getsourcelines',
    'getsourcefile',
]
