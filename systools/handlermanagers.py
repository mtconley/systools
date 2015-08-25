from .misc import in_ipython
from .standardstreams import (StreamToTerminal, 
                             StreamToNotebook, 
                             StreamToFile,
                             StreamToPager,
                             StreamToNull)

class StreamManager(object):
    __registered = {}
    idx = {'log': 0, 'console': 1, 'notebook': 2, 'pager': 3}
    def __init__(self, fd):
        self.__t_out = t_out = StreamToTerminal(fd)
        self.__n_out = n_out = StreamToNotebook(fd)
        self.__f_out = f_out = StreamToFile(fd)
        self.__p_out = p_out = StreamToPager(fd)

        self.handlers = [f_out, t_out, n_out, p_out]

        self.__holding_bay = [StreamToNull(),
                              StreamToNull(),
                              StreamToNull(),
                              StreamToNull()]

    def write(self, message):
        for handler in self.handlers:
            handler.write(message)
            handler.flush()

    def flush(self):
        for handler in self.hadnlers:
            handler.flush()

    def toggle(self, location):
        idx = self.idx[location]
        tmp = self.handlers.pop(idx)
        self.handlers.insert(idx, self.__holding_bay.pop(idx))
        self.__holding_bay.insert(idx, tmp)

    def on(self, location):
        idx = self.idx[location]
        if isinstance(self.handlers[idx], StreamToNull):
            self.toggle(location)

    def off(self, location):
        idx = self.idx[location]
        if not isinstance(self.handlers[idx], StreamToNull):
            self.toggle(location)

