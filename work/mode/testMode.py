#-*-coding:utf-8 -*-
from mode import Mode

testMap = [
        ("des", "asdsad"),
        ("name", "nanmeme"),
]
           
class testMode(Mode):
    _cName = "test"
    attributes = testMap
    def __init__(self):
        super(testMode, self).__init__()
        assert len(self._cName) > 0, ""
 
t = testMode()
a = raw_input()
t.des = "123213"

t.name = "asdasdasdasd"
t.save()
