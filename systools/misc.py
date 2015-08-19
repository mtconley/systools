

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
