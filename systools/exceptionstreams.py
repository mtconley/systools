import os
import sys
import logging
import traceback
from .misc import Registry


class ExceptionToStreamOut(object):
    level = logging.ERROR
    
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''
        
    def __call__(self, exctype, value, traceback):
        self.logger.log(self.log_level, exctype)
        self.logger.log(self.log_level, value)
        for line in traceback.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())
            
    def write(self):
        pass
    
    def flush(self):
        pass
            
        
class IExceptionToStreamOut(ExceptionToStreamOut):
        
    def __call__(self):
        traceback_lines = traceback.format_exception(*sys.exc_info())
        del traceback_lines[1]
        message = ''.join(traceback_lines)
        self.write(message)

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())
        

        
class ExceptionToTerminal(StreamToTerminal):
    def __init__(self, fd=2):
        self.fd = fd
        
    def __call__(self,  exctype, value, traceback):
        self.write(exctype)
        self.write(value)
        for line in traceback.rstrip().splitlines():
            self.write(line.rstrip())
        self.flush()
        
class IExceptionToTerminal(ExceptionToTerminal):
    
    def __call__(self):
        traceback_lines = traceback.format_exception(*sys.exc_info())
        del traceback_lines[1]
        message = ''.join(traceback_lines)
        self.write(message)
        
    

class ExceptionToNotebook(object):
    from IPython.core.interactiveshell import InteractiveShell
    
    def __init__(self):
        pass
    
    def __call__(self):
        return self.InteractiveShell.showtraceback
    
    def write(self):
        pass

    def flush(self):
        pass