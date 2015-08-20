from .misc import in_ipython
import logging

class HandlerManager(object):
    
    def __init__(self):
        pass
        self.output = StreamLogger(stream, level)
        
    def set_log(self, filename):
        
        handler = logging.FileHandler(filename)
        format_string='%(asctime)s:%(levelname)s:%(name)s:%(message)s'
        formatter = logging.Formatter(format_string)
        handler.setFormatter(formatter)
        return handler
        
    def set_notebook(self):
        return sys.stdout
    
    def set_console(self):
        pass
        
    def _in_ipython(self):
        return in_ipython()


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