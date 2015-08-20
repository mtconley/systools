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
    def __init__(self, name, level=logging.INFO):
        self.name = name
        self.handlers = [file_logger, console_logger, notebook_logger]
        self.dummy = DummyLogger()
        
    def create_logger(self, name):
        self.logger = logging.getLogger(name)
        self.logger.handlers = self.handlers
        
    def set_level(self, level):
        self.logger.setLevel(level) 
    
    def on(location):
        idx = {'log': 0, 'console': 1, 'notebook': 2}[location]
        logging._acquireLock()
        try:
            self.logger.handlers.pop(idx)
            self.logger.handlers.insert(idx, self.handlers[idx])
        finally:
            logging._releaseLock()
        
    def off(location):
        idx = {'log': 0, 'console': 1, 'notebook': 2}[location]
        logging._acquireLock()
        try:
            self.logger.handlers.pop(idx)
            self.logger.handlers.insert(idx, self.dummy)
        finally:
            logging._releaseLock()