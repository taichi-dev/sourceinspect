from . import BaseInspector
import tempfile
import atexit
import os


class RemoteInspector(BaseInspector):
    def __init__(self, object):
        self.object = object

    def _source(self):
        object_name = self.object.__name__
        for x in our_ipc_read():
            x = x.strip()
            i = x.find('def ')
            if i == -1:
                continue
            name = x[i + 4:]
            name = name.split(':', maxsplit=1)[0]
            name = name.split('(', maxsplit=1)[0]
            name = name.strip()
            if name == object_name:
                return x
        else:
            raise NameError(
                    f'Could not find source for {object_name}!\n'
                    'Currently `sourceinspect` is only able to inspect'
                    'source of functions yet, sorry!')


def their_ipc_stub(source):
    #print('[SourceInspect] IPC stub got:', source)

    file = 'SI_' + str(os.getpid())
    file = os.path.join(tempfile.gettempdir(), file)
    with open(file, 'a') as f:
            f.write('===\n' + source + '\n')

    if not hasattr(their_ipc_stub, '_did'):
        their_ipc_stub._did = '_did'
        atexit.register(os.unlink, file)


def our_ipc_read():
    file = 'SI_' + str(os.getppid())
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

    __import__("sourceinspect").remote.hack(globals())')

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
    globals['InteractiveInterpreter'].runsource = new_runsource
