import os
import inspect
import logging
from IPython.core.interactiveshell import InteractiveShell
pub = InteractiveShell.instance().display_pub

def in_ipython():
    """Identify environment as IPython or not

    Retuns `bool`
    """
    try:
        __IPYTHON__
        return True
    except:
        return False

def in_notebook():
    """Identify IPython envinronment as notebook
    """
    if in_ipython():
        ip = get_ipython()
        ipynb = IPython.kernel.zmq.zmqshell.ZMQInteractiveShell
        if isinstance(ip.instance(), ipynb):
            return True
        else:
            return False
    else:
        return False

def clear_output(wait=False):
    stream = pub.pub_socket
    parent = pub.parent_header
    indent = pub.topic
    content = dict(False=False)
    msg = u'clear_output'
    pub.session.send(stream, msg, content, parent, indent)

def clear():
    os.system('clear')

def clear_root_logger():
    root = logging.getLogger()
    
    while len(root.handlers):
        root.removeHandler(root.handlers[0])

def rm(filename):
    os.system('rm {}'.format(filename))

def isbooliter(pattern):
    """Identify if patter is list of bools
    Returns `bool`
    """
    return all(map(lambda x: isinstance(x, bool), pattern))

def isboolswitch(pattern):
    """Identify if list is [True, False]
    """
    return isbooliter(pattern) and len(pattern)==2 and sum(pattern) == 1


class Registry(object):
    def __init__(self, args=None):
        """Register a set of variables to restore at a later time in the session

        Parameters
        ----------
            args : `tuple`
                args is a tuple of tuples.  Each tuple in args will be used to
                make the registery dictionary

        Example
        -------
        >>> restore = Registry(('ipout', sys.stdout), ('iperr', sys.stderr))
        >>> restore.ipout
            <open file '<stdout>', mode 'w' at 0x10028e150>
        >>> restore.add('test', 'response')
        >>> restore
            Registered Variables:
                test
                ipout
                    iperr
        >>> restore.remove('test')
        >>> restore
            Registered Variables:
                ipout
                iperr
        """
        self.__registry = {}
        self.__index = {}
        self.__idx = 1
        if args and len(args) == 1:
            self.add(args)
        elif args and len(args) > 1:
            self.add_from(args)

    def add(self, pair):
        key, value = pair
        self.__registry[key] = self.__registry.get(key, value)
        self.__index[self.__idx] = key
        self.__index[key] = self.__idx
        #self.__dict__.update(self.__registry)
        self.__idx += 1

    def add_from(self, pairs):
        for pair in pairs:
            self.add(pair)

    def remove(self, key):
        self.__registry.pop(key)
        self.__dict__.pop(key)
        __idx = self.__index.pop(key)
        self.__index.pop(__idx)

    def __getitem__(self, idx):
        if isinstance(idx, int):
            key = self.__index[idx]
        else:
            key = idx
        return self.__registry[key]

    def __repr__(self):
        return 'Registered Variables:\n\t'+ '\n\t'.join(self.__registry.keys())


class Namespace(object):
    __registry = {}
    __index = {}
    __idx = 1
    def __init__(self, *args):
        """Borg version of Registery
        """
        for arg in args:
            self.add(arg)

    def add(self, pair):
        key, value = pair
        self.__registry[key] = self.__registry.get(key, value)
        self.__index[self.__idx] = key
        self.__index[key] = self.__idx
        self.__dict__.update(self.__registry)
        self.__idx += 1

    def remove(self, key):
        self.__registry.pop(key)
        self.__dict__.pop(key)
        __idx = self.__index.pop(key)
        self.__index.pop(__idx)

    def __getitem__(self, idx):
        if isinstance(idx, int):
            key = self.__index[idx]
        else:
            key = idx
        return self.__registry[key]

    def __repr__(self):
        return 'Registered Variables:\n\t'+ '\n\t'.join(self.__registry.keys())