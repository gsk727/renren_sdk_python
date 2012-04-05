#-*- coding:utf-8 -*-
"""
需要做一些定义1：xx
"""


import pymongo
from bson import binary
db = pymongo.Connection("127.0.0.1", 27017).app


db.base.remove()
db.base.save({
    "name": u"北京1A",
    "des": u"1A",
    "stuff": ["testA@test.com", "AA@test.com", ],
    })

db.base.save({
    "name": u"北京2B",
    "des": u"2B",
    "stuff": ["testB@test.com", "AB@test.com", ],
    })

import time
import md5
db.user.remove()

db.user.save({
    "email": "testB@test.com",
    "name": "testB",
    "begin": time.time() - 60 * 60 * 24 * 365 * 2,
    "end": None,
    "role": u"1:程序员",
    "des": u"后台程序",
    "depart": u"程序",
    "password": binary.Binary(md5.md5("123").digest()),
    "status": "1\:on",
    "permission": ["base", ],
    "base": u"北京1A",
    })

db.user.save({
    "email": "testA@test.com",
    "name": "testA",
    "begin": time.time() - 60 * 60 * 24 * 365 * 10,
    "end": None,
    "role": u"2:策划",
    "des": u"2:策划",
    "depart": u"项目1",
    "password": binary.Binary(md5.md5("123").digest()),
    "status": "1:on",
    "permission": ["air", ],
    "base": u"北京2B",
    })
