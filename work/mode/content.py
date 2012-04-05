#-*-coding: utf-8 -*-
from mode import Mode

contentMap = [
    ("id",  u"序号"), 
    ("name", u"名称"),
    ("title", u"标题"),
    ("stuff", u"员工"), # 怎么生成一个URL
    ("begin", u"创建日期"),
    ("content", u"内容"),
    ("author_name", u"作者姓名"),
    ("author_email", "email"),
]

class ContentMode(Mode):
    _cName = "content"
    attributes = contentMap
    database = "app"
    keys = ("id", )
    def __init__(self):
        super(ContentMode, self).__init__()

    def insert(self):
        """ 
        只是意思上要生成ID,至于ID的可能会赋予更多的含义
        """
        print self.doc
        try:
            maxID = int(self.collection.find().sort([("id", -1)])[0].get("id", 1))
        except:
            maxID = 1

        self.doc["id"] = maxID + 1
        super(ContentMode, self).insert()
 
