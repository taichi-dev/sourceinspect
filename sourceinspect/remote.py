from . import BaseInspector
import tempfile
import atexit
import os


class RemoteInspector(BaseInspector):
    def __init__(self, object):
        self.object = object
        from .code import find_interactive_source
        self.__dict__.update(
                find_interactive_source(self.object, our_ipc_read()))


def their_ipc_stub(source):
    #print('[SourceInspect] IPC stub got:', source)

    file = 'SourceInspect_' + str(os.getpid())
    file = os.path.join(tempfile.gettempdir(), file)
    with open(file, 'a') as f:
            f.write('===\n' + source + '\n')

    if not hasattr(their_ipc_stub, '_did'):
        their_ipc_stub._did = '_did'
        atexit.register(os.unlink, file)


def our_ipc_read():
    file = 'SourceInspect_' + str(os.getppid())
    file = os.path.join(tempfile.gettempdir(), file)
    try:
        with open(file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        raise OSError('Could not retrive source code!\n'
                + get_error_message())

    return reversed(content.split('==='))


def get_error_message():
    return f'''
To make RemoteInspector functional, please append the following line:

    __import__("sourceinspect.remote").remote.hack(globals())')

to file "{__import__("code").__file__}".
'''


def hack(globals):
    import functools
    old_runsource = globals['InteractiveInterpreter'].runsource

    @functools.wraps(old_runsource)
    def new_runsource(self, source, *args, **kwargs):
        their_ipc_stub(source)
        return old_runsource(self, source, *args, **kwargs)

    #print('[SourceInspect] Starting...')
    new_runsource._is_remote_hook = 1
    globals['InteractiveInterpreter'].runsource = new_runsource
