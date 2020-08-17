import tempfile
import atexit
import sys
import os


def their_ipc_stub(source):
    file = 'SI_IPC_' + str(os.getpid()) + '.py'
    file = os.path.join(tempfile.gettempdir(), file)
    with open(file, 'a') as f:
        if source[-1:] != '\n':
            source = source + '\n'
        f.write(source)

    if not hasattr(their_ipc_stub, '_si_did'):
        their_ipc_stub._si_did = '_Did'
        atexit.register(os.unlink, file)


def remote_getfile(object):
    file = 'SI_IPC_' + str(os.getppid()) + '.py'
    file = os.path.join(tempfile.gettempdir(), file)
    if not os.path.exists(file):
        message = get_error_message()
        print(message)
        raise IOError(message)

    with open(file, 'r') as f:
        content = f.read()

    try:
        return remote_getfile._si_cache[content]
    except KeyError:
        pass

    fd, name = tempfile.mkstemp(prefix='SI_IDLE_', suffix='.py')
    os.close(fd)
    with open(name, 'w') as f:
        f.write(content)

    atexit.register(os.unlink, name)
    remote_getfile._si_cache[content] = name

    return name

remote_getfile._si_cache = {}


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

    new_runsource._is_remote_hook = 1
    globals['InteractiveInterpreter'].runsource = new_runsource
