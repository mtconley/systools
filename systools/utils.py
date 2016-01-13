# -*- coding: utf-8 -*-

import ast
from datetime import datetime
import errno
import os
import shutil
import sys
import re

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
        self.fullpath = self._join(self.root, self.name)

    def add_date(self):
        datestr = datetime.now().strftime('%Y%m%d')
        self.name = datestr + '_' + self.name

    def make_tree(self, template_dir, dir_dict):
        if not (template_dir or self._copy_template(template_dir)):
            self._mktree(self.name, dir_dict)

    def write(self, data, location):
        location = self._join(self.fullpath, location)
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


    
    # def __to_pyfile(self):
    #     filename = self.root
    #     node = ast.parse(open(filename,'r').read())
    #     filename = os.path.basename(filename)
    #     result = {}
    #     if hasattr(node, 'body'):
    #         for func in node.body:
    #             function = {'name': None, 'comment': None, 'args': None}
    #             if hasattr(func, 'name'):
    #                 function['name'] = func.name
    #             if hasattr(func, 'arg') and hasattr(func.arg, 'arg'):
    #                 function['args'] = [arg.id for arg in func.args.args]
    #             if hasattr(func, 'body') and hasattr(func.body[0], 'value'):
    #                 expr = func.body[0].value
    #                 if hasattr(expr, 's'):
    #                     function['comment'] = expr.s
    #             result[function['name']] = function
    #     if None in result:
    #         result.pop(None)
    #     self.functions = result

class Node(object):
    def __init__(self, name, prioritytype=type):
        self.name = name
        self.children = []
        self.count = 0
        self.prioritytype = prioritytype
        
    def add(self, node):
        self.children.append(node)
        self.count += 1
        
    def pop(self, index=0):
        self.count -= 1
        return self.children.pop(index)
    
    def display(self, indent=0, row=[]):
        row = row if row else []
        
        if indent == 0:
            print self.name
            
        nchildren = len(self.children)
        
        keys = sorted(self.children, key=lambda x: x.name)
        keys = sorted(keys, key=lambda x: not isinstance(x, self.prioritytype))
        
        for ix, node in enumerate(keys):
            row.append(1)
            if nchildren - ix == 1: row[indent] = 0
            print self._pprinter(row) + str(node.name)
            node.display(indent+1, row)
            row.pop()
    
    def find(self, pattern):
        self.response = self._search(pattern)
        if self.response:
            self.response.display()
        else:
            print 'Pattern, {}, not found'.format(pattern)
                
            
    def _search(self, pattern, match=False):
        match = self._match(pattern) or match
        source = Node(self.name)
        
        for child in self.children:
            result = child._search(pattern, match)
            if result != None or match: source.add(result)
        else:
            if match: return source
            
        if len(source) > 0 or match:
            return source
    
    def _match(self, pattern):
        return len(re.findall(pattern, repr(self.name))) > 0
    
    def _pprinter(self, row):
        symbols = [['   ', '│  '], ['└──', '├──']]   
        nrow = len(row)
        prompt = ''
        for ix, element in enumerate(row):
            last = nrow - ix == 1
            prompt += symbols[last][element]

        return prompt
    
    def __len__(self):
        return self.count




class FileSystemObect(Node):
    def __init__(self, root, prioritytype=type):
        if root.startswith('~'):
            self.root = os.path.expanduser(root)
        elif os.path.isabs(root):
            self.root = root
        else:
            self.root = os.path.abspath(root)
        self.name = os.path.basename(root)
        super(FileSystemObect, self).__init__(self.name, prioritytype)
        self._add_children()
        
    def _add_children(self):
        pass



class Folder(FileSystemObect):
    def __init__(self, root):
        super(Folder, self).__init__(root, Folder)
        
    def _add_children(self):
        for item in os.listdir(self.root):
            path = os.path.join(self.root, item)
            if os.path.isdir(path):
                child = Folder(path)
                self.add(child)
            elif os.path.isfile(path):
                child = File(path)
                self.add(child)



class File(FileSystemObect):
    def __init__(self, root):
        super(File, self).__init__(root, Folder)



class Module(Folder):
    def _add_children(self):
        for item in os.listdir(self.root):
            path = os.path.join(self.root, item)
            if os.path.isdir(path):
                child = Folder(path)
                self.add(child)
            elif os.path.isfile(path) and path.endswith('.py'):
                child = PyFile(path)
                self.add(child)



class PyFile(File):
    def _add_children(self):
        ast_node = ast.parse(open(self.root,'r').read())
        functions = filter(lambda x: isinstance(x, ast.FunctionDef), ast_node.body)
        for func in functions:
            child = FunctionDef(func.name+'()')
            self.add(child)
        classes = filter(lambda x: isinstance(x, ast.ClassDef), ast_node.body)
        for cls in classes:
            child = FunctionDef(cls.name)
            self.add(child)



class ClassDef(Node):
    pass



class FunctionDef(Node):
    pass


def module_dive(module_name):
    exec 'import {0} as module'.format(module_name)
    root = os.path.dirname(module.__file__)
    return Module(root)