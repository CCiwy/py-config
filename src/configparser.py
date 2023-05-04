#!/usr/bin/env python
#-*- coding: utf-8 -*-

__license__ = "MIT"

__author__ = "Quesnok"

# Import Built-Ins

import os
import pathlib
import types
import json

basepath = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
basedir = os.path.dirname(os.path.abspath(basepath)) 

def import_string(import_name):
    """ this is pallets.werkzeug utils.
        see: https://github.com/pallets/werkzeug/blob/main/src/werkzeug/utils.py

        copied it since we only need this one function
    """
    # might need to replace parts of name if its path/PosixPathV
    try:
        __import__(import_name)
    except ImportError:
        raise

    module_name, obj_name = import_name.split(".", 1)
    module = __import__(module_name,  globals(), locals(), [obj_name])

    try:
        return getattr(module, obj_name)
    except AttributeError as e:
        raise ImportError(e) from None


class Config(dict):
    """ dict-like class to hold key/value pairs for application configurations.
        This is inspired by flask.config
    """

    def __init__(self, root_path='') -> None:
        # root path could be PosixPath
        if not len(root_path):
            root_path = basedir

        self.root_path = root_path

    
    def from_json(self, file_path):
        """ read the contents of a json file and parse its key/value pairs.
            be carefull with nested entries
        """
        filename = os.path.join(self.root_path, file_path)
        with open(filename, 'r') as f:
            content = json.load(f)
            self._from_dict(content)


    def from_dict(self, mapping):
        self._dict_keys_are_strings(mapping)
        self._from_dict(mapping)

    def _dict_keys_are_strings(self, mapping):
        if not all([isinstance(k, str) for k in mapping.keys()]):
            raise TypeError('config keys must be strings')

        dict_values = [v for v in mapping.values() if isinstance(v, dict)]
        if dict_values:
            for dv in dict_values:
                self._dict_keys_are_strings(dv)


    def _from_dict(self, mapping):
        for key, value in mapping.items():
            if not key.isupper():
                key = key.upper()
            self._set(key, value)
        

    def from_pyfile(self, file_path):
        """ read the contents of a python file and parse its key/value pairs
            use exec to parse values that are results of functions, eg.
            os.getenv, os.path ...
        """
        filename = os.path.join(self.root_path, file_path)
        target = types.ModuleType("config")
        target.__file__ = filename
        try:
            with open(filename, 'rb') as f:
                exec(compile(f.read(), filename, "exec"), target.__dict__)

        except OSError as e:
            raise

        self.from_obj(target)


    def from_obj(self, obj):
        if isinstance(obj, str):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                value = getattr(obj, key)
                self._set(key, value)


    def _set(self, key, value):
        """ set key/value pair.
            - keys should be stored so that they can get retrieved like
                config.KEY or config.get("KEY") or config["KEY"]

            - should store everything as string, unless its numeric

            - keys must be string
            

        """
        #not sure if needed since always should be called after parsing?
        if not isinstance(key, str):
            raise TypeError(f'config keys must be string, not {type(key)}')

        
           

        # check if result is numeric, else parse to string
        if not isinstance(value, (int, float, complex, dict)):
            value = str(value)

        # set value
        self[key] = value
        setattr(self, key, value)

