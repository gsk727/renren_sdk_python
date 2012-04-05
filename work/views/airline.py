#-*- coding:utf-8 -*-
"""
此处的数据储存使用文档
mongodb：没有找到位一个字典添加key的语句，所以使用了数组的数据结构
"""
import re
from flask import Blueprint, render_template
from common import getDB
from flask import request, jsonify

from util import synchronize, getMode
from mode.airline import airlineMap, AirlineMode

db = getDB("app")
airlineView = Blueprint("airline", __name__, url_prefix="/airline")


@airlineView.route("/", defaults={"base": None}, methods=["GET", ])
@airlineView.route("/<base>", methods=["GET", ])
def get(base):
    if base is None:
        datas = db.base.find({"airlines":{"$exists":1}}, {"airlines":1, "_id":0, "name":1})
    else:
       regx = re.compile(base, re.IGNORECASE)
       datas = db.base.find({"name": regx}, {"_id":0, "airlines":1, "name":1})

    dType = request.args.get("dType", None) 
    if isinstance(dType, basestring) and dType.lower() == "json":
        return jsonify(message = datas.distinct("airlines.name"))

    data = []
    for d in datas:
        t = d.get("airlines",[])
        for x in t:
            x["base"]=d["name"]
        data.extend(t)


    return render_template("showTable.html", 
                     data=data, 
                     tableMap=airlineMap, 
                     addURL="airline.add",
                     updateURL="airline.update",
                     checkType="airline")


@airlineView.route("/", methods=["POST",])
def update():
    updateInfo = getMode(AirlineMode)

    for k, _, checkFun in airlineMap:
        updateInfo[k] = request.form.get(k, "").strip() 
        msg = checkFun(**updateInfo)
        if msg != "ok":
           return jsonify(message=msg)

    updateInfo.update()
    return jsonify(message="ok")


@airlineView.route("/add", methods=["POST", ])
@synchronize
def add():
    addInfo = {}
    for k, _, checkFun in airlineMap:
        addInfo[k] = request.form.get(k, "").strip() 
        msg = checkFun(**addInfo)
        if msg != "ok":
           return jsonify(message=msg)

    db.base.update({"name": addInfo.pop("base")}, {"$push": {"airlines": addInfo}}, True)
    return jsonify(message="ok")

