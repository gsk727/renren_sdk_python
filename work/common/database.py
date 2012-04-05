#-*- coding:utf-8 -*-
from pymongo import database

class MyDB(database.DataBase):
    def __init__(self, connection, name):
        super(database.DataBase, self).__init__(connection, name)

    def find(mode):
        pass
     

