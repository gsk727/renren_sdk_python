#-*- coding:utf-8 -*-
from flask import Blueprint
from common import getDB
from flask import  render_template


airView = Blueprint("air", __name__, url_prefix="/air")
db = getDB("app")


#@airView.before_request # flask.doc => 12.3
#def air_bReq():
#    """
#    这里需要完成用户登录和用户权限检测
#    """
#    if not session.get("isLogined"):
#        return render_template_string(u"<a href={{ url_for('login.login_get') }} >  请登录啊</a>") 
#    elif "userid" in session:
#        g.power = db.user.find_one({"id":session["userid"], "power.air.operator":{"$exists":True}}, {"power":1, "_id":0})
#        if not g.power or "r" not in g.power["power"]["air"]["operator"]:
#            return jsonify(message = u"你的没有权限的")
#        
#        flash("你的权限是%s", g.curPower)

@airView.route("/", methods=["GET", ])
def air_get():
    """
    需要读权限
    """
    return render_template("air.html")

@airView.route("/<air_id>", methods=["GET",])
def air_getbyID(air_id):
    airInfo = db.air.find_one({"id":air_id}, {"_id":0})    
    #if airInfo is None:
    #    return "没有"
    airInfo =[ {"a":1111, "devList":(1, 2, 3), "parent":"本拉登"}, {"a":222, "devList":(1, 2, 3), "parent":"小不是"} ]
    return render_template("air_show.html", airInfo=airInfo)


@airView.route("/", methods=["POST",])
def air_post():
    #air_name = request.form["airName"]
    return "asdas"
