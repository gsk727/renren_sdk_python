#-*- coding:utf-8 -*-
"""
"""
import re
from mode import Mode
from common import getDB
db = getDB("app")
 

def _checkBase(base, **args):
    regx = re.compile(base, re.IGNORECASE)
    if not db.base.find({"name": regx}):
        return u"不存在的基地名称"
    return "ok"


def _checkAirline(base, name, **args):
    regx = re.compile(base, re.IGNORECASE)
    if  db.base.find_one({"airlines.name": {"$in": [name, ]}, "name": regx}):
        return u"存在的航班, 不能添加"
    return "ok"


def _checkAirStatus(name, status, **args):
    """从一个状态到另位一个状态是否合法
    """ 
    db.base.find({}, {"airlines:%s"%(name, ): 1})
    return "ok"


def _checkDefault(**params):
    """默认的
    """
    return "ok"


airlineMap = [
    ("base", u"基地", _checkBase),
    ("begin", u"进入时间", _checkDefault),
    ("end",   u"离开时间", _checkDefault),
    ("name", u"航班编号", _checkAirline),
    ("status", u"状态", _checkAirStatus),
    ("sites", u"座位", _checkDefault),
    ("mode", u"型号", _checkDefault),
   ]


class AirlineMode(Mode):
    _cName = "airline"
    database = "app"
    attributes = airlineMap
    keys = ("name", )
    def __init__(self):
        super(AirlineMode, self).__init__()

