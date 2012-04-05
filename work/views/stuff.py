#-*- coding:utf-8 -*-
"""
职员视图的方法
/stuff/ 获取所有的员工
/stuff/name: 获取制定员工的名字
/stuff/ post :  更新员工
/stuff/add ：添加员工

"""
import md5
from bson import binary 
from flask import Blueprint, request
from flask import jsonify, render_template
import re
from flaskext.babel import gettext, lazy_gettext as _
from flask import redirect, url_for

from flask import g
from mode.stuff import StuffMode
from util import *
from forms.stuff import StuffAddForm, StuffUpdateForm


stuffView = Blueprint("stuff", __name__, url_prefix="/stuff")


@stuffView.route("/", defaults={"base": None})
@stuffView.route("/<base>", methods=["GET", ])
def get(base):
    """根据职员email吧，获取职员(用户)的详细信息  
        职员和用户，管理员都被看成是用户
    """
    regx = re.compile("^%s$"%(base, ), re.IGNORECASE)
    data = None
    updateFrm = StuffUpdateForm()
    addFrm = StuffAddForm()
    data = db.user.find({"base": regx}, {"_id": 0, "password": 0})

    addURL=".".join(("stuff", "add"))
    updateURL = ".".join(("stuff", "update"))
    return render_template("base.html",
                    data=data,
                    addForm = addFrm,
                    updateForm = updateFrm,
                    addURL= url_for("stuff.add", base=base ), 
                    updateURL=url_for("stuff.update"),
                    checkType="stuff"
        )


@stuffView.route("/", methods=["POST", ])
def update():
    """更新存在员工的信息, 可能员工的某些信息不能更新
    """
    updateFrm = StuffUpdateForm()
    if updateFrm.validate_on_submit():     # 在此处验证表单
        m = getMode(StuffMode)
        m.query.update({"number": updateFrm.number.data})
        m.doc.update(updateFrm.asDict())
        m.update()
        flash(_(u"成功更新"), "success") 
    return render_template("update.html", updateForm = updateFrm, updateURL=url_for("stuff.update"))


@stuffView.route("/<base>/add", methods=["POST", ])
def add(base):
    """添加员工的信息
        对一些信息做必要的初始化
    """
    msg = "ok"
    addFrm = StuffAddForm()
    if addFrm.validate_on_submit():     # 在此处验证表单
        sm = getMode(StuffMode)
        sm.doc.update(addFrm.asDict())
        sm.doc.update({"base": base})
        sm.password = binary.Binary(md5.md5("123456").digest())
        err = sm.insert()
        flash(_(u"添加成功"), "success")
    return render_template("add.html", addForm = addFrm, addURL = url_for("stuff.add", base=base))
