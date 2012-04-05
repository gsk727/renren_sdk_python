#-*- coding:utf-8 -*-
from mode import Mode

deviceMap = [
            ("name", u"名字"),
            ("base", u"基地"),
            ("airline", u"航班"),
            ("status", u"状态"),
            ("des", u"描述", ),
            ("local", u"实际所在地"),
            ("content", u"内容"),
            ("histroy", u"历史记录"),
]

class DeviceMode(Mode):
    _cName = "device"
    attributes = deviceMap
    database = "app"
    keys = ("name", )

    def __init__(self):
        super(DeviceMode, self).__init__()

