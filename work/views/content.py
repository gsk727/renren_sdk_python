#-*- coding: utf-8 -*-
from flask import Blueprint, render_template
from mode.content import contentMap, ContentMode
from flask import request, jsonify
from util import synchronize, getMode
from common import getDB


db = getDB("app")
contentView = Blueprint("content", __name__, url_prefix="/device/content")


@contentView.route("/", defaults={"cid":None})
@contentView.route("/<int:cid>", methods=["GET", ])
def get(cid):
    if cid is None:
        data = db.content.find({}, {"_id":0})
    else:
        data = db.content.find({"id":cid}, {"_id":0})

    return render_template("showTable.html",
                        data=data,
						tableMap=contentMap,
						addURL="content.add",
						updateURL="content.update",
                        checkType="content",
            )


@contentView.route("/add", methods=["POST",])
@synchronize
def add():
    """
    """
    content = ContentMode()
    for k, _, in contentMap:
        content[k] = request.form.get(k, "").strip() 
 
    content.insert()
    return jsonify(message="ok")


@contentView.route("/", methods=["POST", ])
def update():
    """
    数据的更新
    """
    updateInfo = getMode(ContentMode)
    for k, _, in contentMap:
        updateInfo[k] = request.form.get(k, "").strip()
    
    updateInfo.query = {"title":updateInfo.title} 
    updateInfo.update() 
    # db.content.update({"title":updateInfo["title"]}, updateInfo)
    return jsonify(message="ok")

