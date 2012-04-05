#-*-coding: utf-8 -*-

from flask import Blueprint

class BaseMethod(object):
    def __init__(self):
        pass

    def get(self):
        pass

    def update(self):
        pass

    def add(self):
        pass


class BaseBlueprint(BaseMethod, Blueprint):
    def __init__(self,module, name, url_prefix):
       super(BaseBlueprint, self).__init__(module, name, url_prefix, url_prefix) 

    
    
