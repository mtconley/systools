import os
import sys
import logging
import traceback
from .misc import Registry

class Stream(logging.StreamHandler):
    levels = {1: (logging.INFO, 'INFO'), 2: (logging.ERROR, 'ERROR')}

    def write(self, message):

        message = message.strip('\n')
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
    streamers = Registry({1: sys.__stdout__, 2: sys.__stderr__}.items())
    
    def __init__(self, file_desc=1):
        
        stream = self.streamers[file_desc]
        super(self.__class__, self).__init__(stream)
        self.level, self.levelname = self.levels[file_desc]


class StreamToNotebook(Stream):
    streamers = Registry({1: sys.stdout, 2: sys.stderr}.items())
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
        self.streamname = 'StreamToPager'
 
    

class StreamToFile(Stream):
    
    def __init__(self, file_desc=1):
        
        self.level, self.levelname = self.levels[file_desc]
        filename = 'out.log'
        
        super(self.__class__, self).__init__(open(filename, 'a'))
        self.set_format()
        self.streamname = 'StreamToFile'
        
    def set_format(self):
        fmt = '%(asctime)s: %(levelname)-5s: %(name)s: %(message)s'
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
       
class StreamToNull(object):
    def __init__(self):
        pass

    def write(self, message):
        pass

    def flush(self):
        pass

    def close(self):
        pass
