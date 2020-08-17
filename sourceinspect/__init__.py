import inspect
import sys


def our_findsource(object):
    from .remote import remote_findsource
    return remote_findsource(object)


class InspectMock():
    def __enter__(self):
        inspect._si_old_findsource = inspect.findsource
        inspect.findsource = our_findsource
        return self

    def __exit__(self, *_):
        inspect.findsource = inspect._si_old_findsource
        del inspect._si_old_findsource


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
