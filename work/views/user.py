#-*- coding:utf-8 -*-
"""
登录的处理, session 储存到数据库, copy cookie认倒霉吧
"""
import md5
from bson import binary

from flask import jsonify
from flask import Blueprint
from flask import url_for, redirect, render_template, request, session, render_template_string

from common import getDB
from forms.account import LoginForm, EditPasswordForm

db = getDB("app")
userView = Blueprint("user", __name__, url_prefix="/user", 
                    static_folder="static"    
            )


@userView.route("/show", methods=["GET"])
def show_self():
    """
    自己查看自己的信息，需要验证用户名和密码 
    """
    name = session.get("name", None)
    res = db.user.find_one({"name": name},  {"_id": 0})
    # 测试的用户显示，这一部分内容会被丢到一个div显示
    return render_template_string(
                                "{% import 'user_macro.html' as user %}\
                                    {{ user.user_self_show(res) }}\
                                ",
                                  res = res
                                  )
    return render_template_string(u"<lable> 用户名字 </lable> <h1> %s </h1> <label> 权限 </lable> <h1> %s</h1>\
                                    <br><br><br><br>11111"
                                  %(res["name"], res["power"]))


@userView.route("/editpassword", methods=["GET", "POST"])
def user_edit_password():
    form = EditPasswordForm()
    if form.validate_on_submit():
        username = session["name"]
        op = form.originPassword.data
        if not db.user.find_and_modify(query = {"name": username, "password": binary.Binary(md5.md5(op).digest())},
                                       update={"$set": {"password": binary.Binary(md5.md5(form.newPassword.data).digest())}}, 
                                       ):
            return u"密码错误， 就是不对"
        else:
            return u"修改成功, 自己刷新回去吧"
    return render_template_string("{% from 'form_macro.html' import render_errors %}\
        <form method='post' action={{ url_for('user.user_edit_password') }} >\
        {{ form.hidden_tag() }} \
        {{ form.originPassword.label }}\
        {{ form.originPassword }} {{ render_errors(form.originPassword) }} <br>\
        {{ form.newPassword.label }}\
        {{ form.newPassword }} {{ render_errors(form.newPassword) }}<br>\
        {{ form.rePassword.label }}\
        {{ form.rePassword }} {{ render_errors(form.rePassword) }} <br>\
        {{ form.submit }} \
        </form>", form=form)


@userView.route("/",  methods=["GET", "POST"])
def get():
    """返回登录界面
    """
    if session.get("name"):
       return redirect(url_for("base.get_all"))
   
    print request.args.get("next", None)

    form = LoginForm(login=request.args.get("username", None),
                     next=request.args.get("next", None))

    if form.validate_on_submit():
        userInfo = db.user.find_one({"name": form.username.data,
                                 "password": binary.Binary(md5.md5(form.password.data).digest())},
                                {"_id": 0})

        if userInfo is None:
            return jsonify(message=u"用户名字或密码错误")

        session["logined"] = True
        session["name"] = userInfo["name"]
        #if "/user/" == url_for(request.url_rule, **request.view_args):
       # return "121212"
        print request.url
        return redirect(form.next.data)

        return jsonify(message="ok")
    return render_template("login.html", form=form)


@userView.route("/logout", methods=["GET",])
def logout():
    if "name" in session:
        session.pop("name")
    return redirect(url_for("index"))


@userView.route("/<name>", methods=["GET", ])
def show(name):
    userInfo = db.user.find_one({"name": name}, {"id":0})
    return render_template("user_show.html", userInfo=userInfo)


@userView.route("/", methods=["POST", ])
def login_post():
    """简单的验证用户
    注意:password全部明文
    密码储存:[salt]+password, 现在没有salt, password储存方式：二进制, 十六进制字符刱
    """
    username = request.form.get("username")
    password = request.form.get("password")  # 明文从客户端传送
    # power:权限
    userInfo = db.user.find_one({"name": username,
                                 "password": binary.Binary(md5.md5(password).digest())},
                                {"_id": 0})
    if userInfo is None:
        return jsonify(message="用户名字或密码错误") #  
    if userInfo.get("power", None) == None:
        return jsonify(message="你的没有权限")

    session["logined"] = True
    session["name"] =  userInfo["name"]
    # g.power = userInfo["power"]
    return jsonify(message="ok")


