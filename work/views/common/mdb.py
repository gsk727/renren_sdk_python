#-*- coding:utf-8 -*-
import pymongo
from xml.dom import minidom
from exceptions import Exception
dbs = {}
isInited = False


class CfgException(Exception):
    def __init__(self, *args, **kwargs):
        super(CfgException, self).__init__(*args, **kwargs)


def getText(nodelist, count=0xffffffff):
    """copy from python documentation
        @param count: 获取几个node的值, 默认给了一个32位的数
    """
    rc = []
    for node in nodelist:
        if len(rc) > count:
            break
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data.strip())
    return "".join(rc)


def get_conList():
    """
    simple simple
    """
    cfg = minidom.parse("./dbcfg.xml")
    cons = cfg.getElementsByTagName("connection")
    conList = []
    for con in cons:
        hostdom = con.getElementsByTagName("host")[0]
        host = getText(hostdom.childNodes, 1)

        portdom = con.getElementsByTagName("port")[0]
        port = getText(portdom.childNodes, 1)

        dbdom = con.getElementsByTagName("dbname")[0]
        dbname = getText(dbdom.childNodes, 1)

        cdom = con.getElementsByTagName("collection")
        cnames = []
        for cname in cdom:
            cnames.append(getText(cname.childNodes, 1))

        #dbname = getText(con.getElementsByTagName("dbname")[0].childNodes, 1)
        conList.append((host.strip(), int(port), dbname, cnames))
    return conList


def initDB():
    """
    1个数据库一个链接
    """
    global dbs
    conList = get_conList()  # reload
    for con in conList:
        print con
        dbname = con[2]
        dbs["connection"] = pymongo.Connection(con[0], con[1])
        dbs[dbname] = dbs["connection"][dbname.strip()]
    global isInited
    isInited = True


def getDB(name):
    global isInited
    if not isInited:
        initDB()
    db = dbs.get(name, None)
    assert db is not None, "db" + name + "不存在"
    return db


def swithDB(fromdb, todb, reuse=True):
    """
    @param reuse 使用一个链接
    """
    if fromdb not in dbs:
        raise CfgException("swith db from %s to %s failed" % (fromdb, todb))

    if reuse:
        if todb in dbs:
            return dbs[todb]
        else:
            return dbs[fromdb].connection.todb
    else:
        if fromdb not in dbs or todb not in dbs:
            raise CfgException("db from %s to %s failed" % (fromdb, todb))
        return dbs[todb]

    assert(1 != 1)


if __name__ == "__main__":
    print getDB("app")
