import tempfile
import inspect
import atexit
import sys
import os


def their_ipc_stub(source):
    file = 'SI_IPC_' + str(os.getpid()) + '.py'
    file = os.path.join(tempfile.gettempdir(), file)
    with open(file, 'a') as f:
        if source[-1:] != '\n':
            source = source + '\n'
        f.write(source + '===\n')

    if not hasattr(their_ipc_stub, '_si_did'):
        their_ipc_stub._si_did = '_Did'
        atexit.register(os.unlink, file)


def remote_findsource(object):
    file = 'SI_IPC_' + str(os.getppid() if 'idlelib' in sys.modules else os.getpid()) + '.py'
    file = os.path.join(tempfile.gettempdir(), file)
    if not os.path.exists(file):
        message = get_error_message()
        print(message)
        raise IOError(f'Cannot find file {file}!' + message)

    with open(file, 'r') as f:
        lines = f.read()

    lines = lines.split('===\n')
    for lnum, line in reversed(list(enumerate(lines))):
        try:
            name = line.split('def ', 1)[1]
            name = name.split(':', 1)[0]
            name = name.split('(', 1)[0]
            if name == object.__name__:
                break
        except IndexError:
            pass
    else:
        raise IOError(f'Cannot find source of object `{object.__name__}`')

    return lines, lnum


def get_error_message():
    name = 'SourceInspect'
    if 'taichi' in sys.modules:
        name = 'Taichi'
    return f'''
To make {name} functional in IDLE, please append the following line:

__import__("sourceinspect.remote").remote.hack(globals())

to file "{__import__("code").__file__}".
'''


def hack(globals):
    import functools
    old_runsource = globals['InteractiveInterpreter'].runsource

    @functools.wraps(old_runsource)
    def new_runsource(self, source, *args, **kwargs):
        their_ipc_stub(source)
        return old_runsource(self, source, *args, **kwargs)

    globals['InteractiveInterpreter'].runsource = new_runsource
