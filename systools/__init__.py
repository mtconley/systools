import debug
import exceptionstreams
import handlermanagers
import misc
import pipe
import prompt
import standardstreams
import utils

import pyprind

def _print(self):
    
    progress = floor(self._calc_percent() / 100 * self.bar_width)
    if self.active:
        self._stream_out('\r')
        self._print_progress_bar(progress)
        if self.track:
            self._print_eta()
        if self.item_id:
            self._print_item_id()
        self._stream_flush()
    self.last_progress = progress

pyprind.ProgBar._print = _print