import sys
import os
import shutil
import errno
from datetime import datetime

class Directory(object):
    dir_paths = []
    def __init__(self, name, date=False, root=None):
        """Define and make a new directory"""
        self.name = name.strip().replace(' ', '_')
        self.set_root(root)
        self.set_fullpath()
        if date:
            self.add_date()

    def set_root(self, root):
        if root:
            self.root = root + (1 - root.endswith(os.sep) * os.sep)
        else:
            self.root = os.getcwd()

    def set_dirpaths(self):
        self.dir_paths = [x[0] for x in os.walk(self.fullpath)]

    def set_fullpath(self):
        self.fullpath = self.join(self.root, self.name)

    def add_date(self):
        datestr = datetime.now().strftime('%Y%m%d')
        self.name = datestr + '_' + self.name

    def make_tree(self, template_dir, dir_dict):
        if not (template_dir or self._copy_template(template_dir)):
            self._mktree(self.name, dir_dict)

    def write(self, data, location):
        location = self.join(self.fullpath, location)
        path = os.sep.join(location.split(os.sep)[:-1])
        if path in self.dir_paths:
            with open(location, 'w') as f:
                f.write(data)
        else:
            raise IOError("""{0} must be in: \n{1}
                """.format(path, '\n\t'.join(self.dir_paths)))

    def _copy_template(self, template_dir):
        try:
            shutil.copytree(template_dir, self.fullpath)
            self.set_dirpaths()
            return True
        except (Exception, OSError) as e: # Check if already exists
            if hasattr(e, 'errno') and e.errno == errno.EEXIST and self.isdir(template_dir):
                self.set_dirpaths()
                return True
            else:
                return False

    def _mktree(self, root, dir_dict):
        for path, name in dir_dict.iteritems():
            if not name:
                fullpath = self._join(root, path)
                self._mkdir(fullpath)
            else:
                fullpath = self._join(root, path)
                self._mktree(fullpath, name)
        self.set_dirpaths()

                
    def _mkdir(self, fullpath):
        try:
            os.makedirs(fullpath)
        except OSError as e: # Check if already exists
            if e.errno == errno.EEXIST and self._isdir(fullpath):
                pass
            else: raise

    def _join(self, root, _dir):
        return os.path.join(root, _dir)

    def _isdir(self, _dir):
        return os.path.isdir(_dir)