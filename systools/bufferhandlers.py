import os
import sys
import logging
import traceback
from .misc import Registry


class StreamOut(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    level = logging.INFO
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def emit(self, buf):
        self.write(buf)
        self.flush()
 
    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip()+'\n')
            
    def flush(self):
        self.logger.flush()

class Stream(logging.StreamHandler):
    levels = {1: (logging.INFO, 'INFO'), 2: (logging.ERROR, 'ERROR')}


    def write(self, message):
        log_event = {'msg': message, 'levelno': self.level,
                    'levelname': self.levelname, 'name': self._name}
        record = self.makeRecord(**log_event)
        self.emit(record)
        self.flush()
        self.stream.flush()

        
    def makeRecord(self, **kwargs):
        record = logging.makeLogRecord(kwargs)
        return record
    
    
class StreamToTerminal(Stream):
    streamers = Registry(*{1: sys.__stdout__, 2: sys.__stderr__}.items())
    
    
    def __init__(self, file_desc=1):
        
        stream = self.streamers[file_desc]
        super(self.__class__, self).__init__(stream)
        self.level, self.levelname = self.levels[file_desc]
        

class StreamToNotebook(Stream):
    streamers = Registry(*{1: sys.stdout, 2: sys.stderr}.items())
    def __init__(self, file_desc=1):
        
        stream = self.streamers[file_desc]
        self.level, self.levelname = self.levels[file_desc]
        super(self.__class__, self).__init__(stream)

class PageStream(object):
    import IPython.core.page as page
    def __init__(self):
        pass

    def write(self, message):
        self.page.page(message)

    def flush(self):
        pass

    def close(self):
        pass

class StreamToPager(Stream):
    stream = PageStream
    def __init__(self, file_desc=1):
        
        stream = self.stream()
        self.level, self.levelname = self.levels[file_desc]
        super(self.__class__, self).__init__(stream)
    

class StreamToFile(Stream):
    
    def __init__(self, file_desc=1):
        
        self.level, self.levelname = self.levels[file_desc]
        filename = 'out.log'
        
        super(self.__class__, self).__init__(open(filename, 'a'))
        self.set_format()
        
    def set_format(self):
        fmt = '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
        formatter = logging.Formatter(fmt)
        self.setFormatter(formatter) 

    def close(self):
        """
        Closes the stream.
        """
        self.acquire()
        try:
            try:
                if self.stream:
                    try:
                        self.flush()
                    finally:
                        stream = self.stream
                        self.stream = None
                        if hasattr(stream, "close"):
                            stream.close()
            finally:
                # Issue #19523: call unconditionally to
                # prevent a handler leak when delay is set
                logging.StreamHandler.close(self)
        finally:
            self.release()      
        


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