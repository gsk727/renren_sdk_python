# -*- coding: utf-8  -*-
"""
工具模块
"""
import threading
import weakref
from threading import Lock
from functools import update_wrapper
from flask import session, render_template, g, flash
from common import getDB
from mode import Mode
from flask import redirect, url_for, request

_g_lock = Lock()
db = getDB("app")
_twRef = {}
_localModes = {}


def synchronize(method):
    """
    怒了啊，提供线程同步的装饰器
    """
    def Angry(*args, **kwargs):
        with _g_lock:
            return method(*args, **kwargs)

    return update_wrapper(Angry, method)


def app_verifyUser(**options):
    """
    凑合着用吧。验证用户session
    现在用户的ID， 同时也为Session ID
    我靠，猥琐的一个函数
    """
    fun = []                    # 
    def wrapper(method):
        # fun = method # 这样的fun属于wrapper函数而不是app的变量
        fun.append(method)
        return update_wrapper(default, method)

    def default(**moptions):
        name = session.get("name")
        if name is None:
            return redirect(url_for("user.get", next= request.url))
        userInfo = db.user.find_one({"name": name})
        if not userInfo:
            return redirect(url_for("user.get"), next= request.url)

        if options.get("power", False) and not userInfo.get("power", None):
                return jsonify(message=u"你的没有权限")
        name, pwd = userInfo["name"], userInfo["password"]
        fun[0](**moptions)     # 可以提前返回

    return wrapper


def release_mode(threadRef, name, tid):
    """
    线程“没有”后，ident 将被回收利用
    """
    global __twRef
    if tid in _twRef:
        _twRef.pop(tid)
    if name in _localModes and tid in _localModes[name]:
        _localModes[name].pop(tid)


def getMode(cls, name=None):
    assert issubclass(cls, Mode), u"基类不是Mode"

    t = threading.current_thread()
    tid = t.ident
    if name is None:
        name = cls.__name__

    if tid not in _twRef:   # 一个线程可能多次被调用, 不重复添加
        _twRef[tid] = weakref.ref(t, lambda r, i=tid, name=name: release_mode(r, name, tid))  # 2
    modes = _localModes.setdefault(name, {})  # 1

    return modes.setdefault(tid, cls())