import sys
import logging

class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''
 
    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())
            
    def flush(self):
        pass
            
class Pipe(object):

    __registered = {}
    
    def __init__(self):
        """
        TODO ##########
        Implement polymorphism for use with ipython and python--shell and nb
        IPython nb is not logging errors
        ...
            get_ipython().parent.log
            from IPython.kernel.zmq.iostream import OutStream
        ...
        """

        self.__registered['STDOUT'] = self.__registered.get('STDOUT', sys.stdout)
        self.__registered['STDERR'] = self.__registered.get('STDERR', sys.stderr)

        self.stdout_normal = self.__registered['STDOUT']
        self.stderr_normal = self.__registered['STDERR']

        stdout_logger = logging.getLogger('STDOUT')
        stderr_logger = logging.getLogger('STDERR') 
        
        handler = logging.FileHandler('out.log')
        
        fmt_str = '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
        formatter = logging.Formatter(fmt_str)
        handler.setFormatter(formatter)
        
        stdout_logger.addHandler(handler)
        stderr_logger.addHandler(handler)
        
        stdout_logger.setLevel(logging.DEBUG)
        
        self.stream_out_logger = StreamToLogger(stdout_logger, logging.INFO)
        self.stream_err_logger = StreamToLogger(stderr_logger, logging.ERROR)

    def log(self, *args):
        if len(args) == 0:
            sys.stdout = self.stream_out_logger
            sys.stderr = self.stream_err_logger
        if 'out' in args:
            sys.stdout = self.stream_out_logger
        if 'err' in args:
            sys.stderr = self.stream_err_logger

    def console(self, *args):
        if len(args) == 0:
            sys.stdout = self.stdout_normal
            sys.stderr = self.stderr_normal
        if 'out' in args:
            sys.stdout = self.stdout_normal
        if 'err' in args:
            sys.stderr = self.stderr_normal