#-*-coding: utf-8 -*-

from exceptions import Exception
from mdb import getDB


__all__ = ["getDB", ]

# id collection
__collection4ids = ["base", "air", "device", "content", "default"]


def app_getID(k="default"):
    """{"key":cName, "value":int}
    """
    db = getDB("app")
    v = db.ids.find_and_modify(
            query={"key": k},
            update={"$inc": {"value": 1}},
            upsert=True,
            new=True,
            fileds={"value": 1}
        )["value"]

    return v


class AppException(Exception):
    '''
    异常类
    '''
    pass
