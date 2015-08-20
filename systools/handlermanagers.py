from .misc import in_ipython
import logging
from .standardstreams import (StreamToTerminal, 
                             StreamToNotebook, 
                             StreamToFile,
                             StreamToPager)

class StreamManager(object):
    
    def __init__(self):
        self.t_out = t_out = StreamToTerminal(1)
        self.t_err = t_err = StreamToTerminal(2)
        self.n_out = n_out = StreamToNotebook(1)
        self.n_err = n_err = StreamToNotebook(2)
        self.f_out = f_out = StreamToFile(1)
        self.f_err = f_err = StreamToFile(2)

        self.stdout = LoggerManager('STDOUT')
        self.stderr = LoggerManager('STDERR')

        self.stdout.add_handlers(t_out, n_out, f_out)
        self.stderr.add_handlers(t_err, n_err, f_err)


class LoggerManager(object):
    __registered = {}
    idx = {'log': 0, 'console': 1, 'notebook': 2, 'pager': 3}
    def __init__(self, name, level=logging.INFO):
        self.name = name
        self.dummy = logging.NullHandler()
        self.create_logger(name)
        self.set_level(level)

    def create_logger(self, name):
        self.logger = logging.getLogger(name)

    def set_level(self, level):
        self.logger.level = level
        self.level = level

    def add_handler(self, handler):
        self.logger.addHandler(handler)
    
    def add_handlers(self, *handlers):
        for hdlr in handlers:
            self.add_handler(hdlr)

    def write(self, message):
        self.logger.log(self.level, message)

    def flush(self):
        pass

    def on(location):
        idx = self.idx[location]
        logging._acquireLock()
        try:
            self.logger.handlers.pop(idx)
            self.logger.handlers.insert(idx, self.handlers[idx])
        finally:
            logging._releaseLock()
        
    def off(location):
        idx = self.idx[location]
        logging._acquireLock()
        try:
            self.logger.handlers.pop(idx)
            self.logger.handlers.insert(idx, self.dummy)
        finally:
            logging._releaseLock()