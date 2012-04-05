#-*- coding:utf-8 -*-
"""
"""
from mode import Mode


class BaseMode(Mode):
    _cName = "base"
    database = "app"
    attributes = ["number", "name", "city", "des"]
    keys = ("name", )
    def __init__(self):
        super(BaseMode, self).__init__()

