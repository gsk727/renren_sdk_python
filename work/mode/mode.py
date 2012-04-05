#-*- coding:utf-8 -*-
"""
简单的mode, 存在很多的问题
"""
from threading import local
from common import getDB
from pymongo.collection import Collection

class LocalData(local):
    def __setitem__(self, k, v):
        setattr(self, k, v)

    def __getitem__(self, k):
        return getattr(self, k)

class MetaMode(type):
    """
    Mode的元类，模板
    """
    def __new__(cls, name, bases, attrs):
        super_new = super(MetaMode, cls).__new__
        parents = [b for b in bases if isinstance(b, MetaMode)]
        if not parents:
           return super_new(cls, name, bases, attrs)
 
        o = super_new(cls, name, bases, attrs) 
        
        # 附加属性, 这些属性是静态的属性 
        database =  attrs.get("database", "test")
        o.db = getDB(database)
        
        assert attrs.get("_cName") is not None, "Mode；类需要定义_cName"
        o.collection = o.db[attrs.get("_cName")]
        return o
    

class MyCollectin(Collection):
    pass

class Mode(object):
    """
    分离出来一个collection类吗？
    """
    __metaclass__ = MetaMode

    def __init__(self):
        """
        参数正确性放到子类里面了
        """
        self.doc = {}
        self.query = {}
    def compileQuery(self):
        """
        虚拟函数:生成查询条件
        """
        return dict([(x, self.doc.get(x, "")) for x in self.keys])


    def IsKeysExisted(self):
        """
        virtual.
        主要完成更新，增加数据的时候唯一性检测
        """
        if not hasattr(self, "keys") or len(self.keys) <= 0:
            return False

        query = self.compileQuery() 
        return self.collection.find_one(query) is not None


    def save(self):
        assert len(self.doc) > 0, "先添加数据"
        self.collection.save(self.doc)


    def update(self, keyUpdate = True, **options):
        """
        @params: keyUpdate.  squery 内k-v 是否作为更新的一部分 True:是，False：不是 
        当Fasle的时候，如果keys 在 self.doc中，self.doc 也不会pop keys
        更新根据keys的值
        """
        if keyUpdate:
            self.doc.update(self.query)
        if len(self.query) == 0:    # 默认使用keys作为query
            query = dict([(x, self.doc.get(x, None))  for x in self.keys])
        else:
            query = self.query

        return self.collection.update(query, {"$set":self.doc}, **options)


    def insert(self):
        """
        """
        if self.IsKeysExisted():
            return "EXIST" 
        self.save()


    def find(self, query, fields):
        return self.collection.find(query, fields)


    def find_one(self, query, fields):
        return self.collection.find_one(query, fields)


    def __setattr__(self, key, value):
        if key in self.attributes:
            self.doc[key] = value

        object.__setattr__(self, key, value)

    def __getattr__(self, key):
        if key in self.doc:
            return self.doc[key]
        raise AttributeError("mode %s不存在的属性"%(key,))

    def __enter__(self):
        pass
    def __exit__(self):
        self.clear()

    def clear(self):
        self.doc.clear()
        self.query.clear()

    def __setitem__(self, k, v):
        return setattr(self, k, v)

    def __getitem__(self, k):
        return getattr(self, k)

