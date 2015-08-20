from .misc import in_ipython

class Pipe(object):
    __registered = {}
    
    def __init__(self):
        """
        TODO:
            IPython Notebook overwrites sys.exechook everytime, cannot be customized
            If _in_ipython(), log, notebook, and console need to change showtraceback
            If not _in_ipython(), log, noteboo, and console need to change sys.excepthook
            
            Add suppport for multiple logging (n \choose k) .addHandlers()
        """
        if self._in_ipython():
            from IPython.core.interactiveshell import InteractiveShell
            stdexc = self.InteractiveShell.showtraceback
        else:
            stdexc = sys.excepthook
        
        self.stdout = LoggerManager('stdout', logging.INFO)
        self.stderr = LoggerManager('stderr', logging.ERROR)
        self.stdexc = LoggerManager('stdexc', logging.ERROR)
        self.catch = Catcher() ### Maybe
                                                
        def log_on(self, *fdesc):              
            self._on('log', *fdesc)          
            
        def console_on(self, *fdesc):
            self._on('console', *fdesc)
            
        def notebook_on(self, *fdesc):
            self._on('notebook', *fdesc)
            
        def log_off(self, *fdesc):              
            self._off('log', *fdesc)          
            
        def console_off(self, *fdesc):
            self._off('console', *fdesc)
            
        def notebook_off(self, *fdesc):
            self._off('notebook', *fdesc)
            
        def write_all(self):
            for location in ['log', 'console', 'notebook']:
                self._on(location)
            
        def write_none(self):
            for location in ['log', 'console', 'notebook']:
                self._off(location)
                    
        def _on(self, location, *args):
            if len(args) == 0:
                args = ['out', 'err', 'exc']
            for arg in args:
                {'out': self.stdout.on,
                 'err': self.stderr.on,
                 'exc': self.stdexc.on}.get(arg, self.catch)(location)
                
        def _off(self, location, *args):
            if len(args) == 0:
                args = ['out', 'err', 'exc']
            for arg in args:
                {'out': self.stdout.off,
                 'err': self.stderr.off,
                 'exc': self.stdexc.off}.get(arg, self.catch)(location)
                   
        def _in_ipython(self):
            return in_ipython()