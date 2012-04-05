#-*- coding:utf-8 -*-

from flask import Blueprint, render_template

adminView = Blueprint("admin", __name__, url_prefix="/admin")


@adminView.route("/", methods=["GET", ])
def admin_get():
    return render_template("admin.html")
