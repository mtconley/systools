# -*- coding: utf-8 -*-

import ast
from datetime import datetime
import errno
import os
import shutil
import sys

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

class Class(object):
    pass

class Function(object):
    def __init__(self, data):
        self.name = data.pop('name')
        self.data = data
        self.__dict__.update(data)
    def __repr__(self):
        string = "{}:\n".format(self.name)
        for name, value in self.data.iteritems():
            string += "  {0}:\n ".format(name)
            if value is not None:
                if hasattr(value, '__iter__'):
                    value = [x for line in value for x in line.split()] 
                    for line in value:
                        string += "    {0}\n".format(line)
                else:
                    value = [x for x in value.split('\n') if x != '']
                    if len(value) == 1:
                        line = value[0]
                        string += "    {0}\n".format(line)
                    elif len(value) > 1:
                        for line in value:
                            string += "    {0}\n".format(line)
                    else:
                        string += "    None\n"
            else:
                string += "    None\n"
        return string

class File(object):
    def __init__(self, root):
        self.root = root
        self.name = os.path.basename(root)

    def display(self, indent=0):
        pass


def limb(depth, is_end=True):
    return '{0}  '.format('│') * (depth - 1) + ['├──', '└──'][is_end] * (depth > 0)

class Folder(object):
    def __init__(self, root):
        if root.startswith('~'):
            self.root = os.path.expanduser(root)
        elif os.path.isabs(root):
            self.root = root
        else:
            self.root = os.path.abspath(root)
        self.name = os.path.basename(root)
        self.__get_contents()
        self.__add_subdirectories()
        
    def __get_contents(self):
        contents = [os.path.join(self.root, x) for x in os.listdir(self.root)]
        self.dirs = {os.path.basename(x): None for x in contents if os.path.isdir(x)}
        self.files = {os.path.basename(x): None for x in contents if os.path.isfile(x)}
        
    def __add_subdirectories(self):
        for directory in self.dirs:
            fullpath = os.path.join(self.root, directory)
            self.dirs[directory] = Folder(fullpath)
            self.__dict__[directory] = self.dirs[directory]
        for f in self.files:
            fullpath = os.path.join(self.root, f)
            self.files[f] = File(fullpath)
            if not f.startswith(('__init__', 'files')):
                clean_f = f.strip('.').partition(os.sep)
                self.__dict__[clean_f] = self.files[f]

    def display(self, indent=0, is_end=False):
        print limb(indent, is_end) + self.name
        dirs = sorted(x for x in self.dirs.keys() if not x.startswith('.'))
        nDir = len(dirs)
        fs = sorted(x for x in self.files.keys() if not x.startswith('.'))
        nFile = len(fs)
        for ix, folder in enumerate(dirs):
                self.__dict__[folder].display(indent+1, ((nDir + nFile) - 1) == ix)
        for ix, f in enumerate(fs):
            print limb(indent+1, (nFile - 1) == ix) + f
            self.files[f].display(indent+1)

    """
    def display(self, indent=0):
        for folder in sorted(self.dirs.keys()):
            if not folder.startswith('.'):
                print '\t' * indent + folder
                self.__dict__[folder].display(indent+1)
        for f in sorted(self.files.keys()):
            if not f.startswith('.'):
                print '\t' * indent + f
                self.files[f].display(indent+1)
    """



class Module(Folder):
    def __init__(self, root):
        super(self.__class__, self).__init__(root)
        
    def __get_contents(self):
        contents = [os.path.join(self.root, x) for x in os.listdir(self.root)]
        self.dirs = {os.path.basename(x): None for x in contents if os.path.isdir(x)}
        self.files = {os.path.basename(x): None for x in contents if os.path.isfile(x) and x.endswith('.py')}
        
    def __add_subdirectories(self):
        for directory in self.dirs:
            fullpath = os.path.join(self.root, directory)
            self.dirs[directory] = Module(fullpath)
            self.__dict__[directory] = self.dirs[directory]
        for f in self.files:
            fullpath = os.path.join(self.root, f)
            self.files[f] = PyFile(fullpath)
            if not f.startswith(('__init__', 'files')):
                clean_f = f.strip('.').partition(os.extsep)[0]
                self.__dict__[clean_f] = self.files[f]

    def display(self, indent=0):
        for folder in sorted(self.dirs.keys()):
            print '\t' * indent + folder
            self.__dict__[folder].display(indent+1)
        for f in sorted(self.files.keys()):
            print '\t' * indent, f
            self.files[f].display(indent+1)

class PyFile(File):
    def __init__(self, root):
        self.root = root
        self.name = os.path.basename(root)
        self.__to_pyfile()
        for name, function in self.functions.iteritems():
            self.__dict__[name] = Function(function)
    
    def __to_pyfile(self):
        filename = self.root
        node = ast.parse(open(filename,'r').read())
        filename = os.path.basename(filename)
        result = {}
        if hasattr(node, 'body'):
            for func in node.body:
                function = {'name': None, 'comment': None, 'args': None}
                if hasattr(func, 'name'):
                    function['name'] = func.name
                if hasattr(func, 'arg') and hasattr(func.arg, 'arg'):
                    function['args'] = [arg.id for arg in func.args.args]
                if hasattr(func, 'body') and hasattr(func.body[0], 'value'):
                    expr = func.body[0].value
                    if hasattr(expr, 's'):
                        function['comment'] = expr.s
                result[function['name']] = function
        if None in result:
            result.pop(None)
        self.functions = result

def module_dive(module_name):
    exec 'import {0} as module'.format(module_name)
    root = os.path.dirname(module.__file__)
    return Module(root)