#-*- coding:utf-8 -*-
import copy
from flask import Blueprint
from flask import render_template, request, jsonify
from common import getDB, AppException
from util import app_verifyUser, synchronize, getMode
from mode.device import deviceMap, DeviceMode



MAX_HISTORY_LEN = 5
deviceView = Blueprint("device", __name__, url_prefix="/device")
db = getDB("app")


@deviceView.before_request
@app_verifyUser(power = False)     # 不允许匿名访问
def device_beforeRequest(*args, **kwargs):
    """return会导致后面的route无法调用, nodejs的next() 是个好东西啊
    """
    print "login_beforeQuest"


@deviceView.route("/base/<baseName>", methods=["GET", ])
def get_base(baseName):
    """文档嵌套
    """
    data = db.device.find({"base":baseName}, {"_id":0}) 
    return render_template("showTable.html", 
                     data=data, 
                     tableMap=deviceMap, 
                     addURL="device.add",
                     updateURL="device.update",
                     checkType="device")


@deviceView.route("/<name>", methods=["GET", ])
def get(name):
    """根据设备名字获取设备的信息
    """
    data = db.devices.find({"name":name}, {"_id": 0})
    return render_template("showTable.html", 
                     data=data,
                     tableMap=deviceMap,
                     addURL=None,
                     updateURL="device.update",
                     checkType="device")


@deviceView.route("/add", methods=["POST", ])
@synchronize
def add():
    """用于添加设备,设备编号是唯一的,或者收到添加。
    """
    deviceInfo = getMode(DeviceMode)
    
    # 没有添加验证
    for d, _ in deviceMap:
        deviceInfo[d] = request.form.get(d, "").strip()

    deviceInfo.insert()
    return jsonify(message="ok")


@deviceView.route("/", methods=["POST", ])
def update():
    """用于添加设备,设备编号是唯一的,或者收到添加。
    """
    deviceInfo = getMode(DeviceMode)
    # 没有添加验证
    for d, _ in deviceMap:
        deviceInfo[d] = request.form.get(d)
    
    devID = deviceInfo["devID"]   # 等级设备的时候设备应该有一个唯一的编号了啊
    if devID is None:
        return "没有设备编号"
        # 下面的操作是非线程安全的
        res = db.device.find_one({"devID": devID})
        if res:
            return "重复编号"

    res = db.device.find_one({"name":deviceInfo["name"]}, {"_id":0})
    
    # 过程太繁琐了
    try:
        h = res.pop("histroy")
        index = h[0] = h[0]%MAX_HISTORY_LEN + 1
    except:
        h = [0, ]
        h.extend([{} for x in xrange(0, MAX_HISTORY_LEN)])
        index = h[0] = h[0] % MAX_HISTORY_LEN + 1

    # histroy=[index, {}, {}, {}]最多 MAX_HISTORY_LEN 个， index记录最前面的一个记录
    h[index] = copy.deepcopy(res)  # 递归问题
    res["history"] = h
    res.update(deviceInfo)
    db.device.save(res)
    return jsonify(message="ok")


@deviceView.route("/move", methods=["POST", ])
def device_move():
    """设备从一个飞机到另一个飞机
    1， 飞机s在统一个基地
    2，飞机s不在同一个基地
    3, 设置第一次安装到飞机
    设备迁移历史信息记录的保存和维护
    设备维修历史记录的信息，
    设置现在存有的杂志信息
    """
    tofly = request.form["tofly"]
    frmfly = request.form["fromfly"]
    devID = request.form["devID"]
    devDes = request.form["devDes"]

    frmInfo = db.fly.find_one({"id": frmfly},
                              {"devices": {"$elemMatch": {"$in": [devID, ]}}})
    toInfo = db.fly.find_one({"id": tofly})
    if not frmInfo or not toInfo:
        raise AppException("device_move")

    for index, d in enumerate(frmInfo["devices"]):
        dID, _ = d
        if dID == devID:
            frmInfo["devices"].pop(index)
            break   # 一定要break掉

    toInfo["devices"].append((devID, devDes))

    db.device.update({"id": devID}, {"parent": tofly})
    db.fly.save(toInfo)     # 有_id 的save
    db.fly.save(frmInfo)


@deviceView.route("/add_content/<devID>", methods=["POST", ])
def device_addContent(devID):
    """
    添加制定的内容到设置这是一个断章取义的接口，需要下载到本地吗？
    """
    res = db.device.find_one({"id": devID})
    if not res:
        return "没有"

    cID = request.form["contentID"]
    cDes = request.form["contentDes"]
    res = db.contend.find_one({"id": cID})
    if not res:
        return jsonify(message=u"没有")

    # 这个地方可能会发送具体的内容
    db.device.update({"id": devID}, {"$addToSet": {"content": [cID, cDes, ]}})
