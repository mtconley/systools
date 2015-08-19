

def in_ipython():
    """Identify environment as IPython or not

    Retuns `bool`
    """
    try:
        __IPYTHON__
        return True
    except:
        return False

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
    __registry = {}
    def __init__(self, *args):
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
        for arg in args:
            self.add(arg)

    def add(self, pair):
        key, value = pair
        self.__registry[key] = self.__registry.get(key, value)
        self.__dict__.update(self.__registry)

    def remove(self, key):
        self.__registry.pop(key)
        self.__dict__.pop(key)

    def __repr__(self):
        return 'Registered Variables:\n\t'+ '\n\t'.join(self.__registry.keys())