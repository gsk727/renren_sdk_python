#-*-coding:utf-8 -*-
from flask import Flask, session, g
from flask import redirect, url_for, render_template_string, render_template
from views import deviceView
from views import userView
from views import adminView
from views import airView
from views import baseView
import time
import common
from views import stuffView
from views import taskView, airlineView
from views import contentView
from flaskext.babel import Babel
from flask import request

app = Flask(__name__)
app.register_blueprint(userView)
app.register_blueprint(deviceView)
app.register_blueprint(adminView)
app.register_blueprint(airView)
app.register_blueprint(stuffView)
app.register_blueprint(baseView)
app.register_blueprint(taskView)
app.register_blueprint(airlineView)
app.register_blueprint(contentView)

babel = Babel(app)

db = common.getDB("app")


@app.errorhandler(405)
def method_not_allowed(error):
    rs = []
    for r in app.url_map.iter_rules():
        ts = str(r).replace("<", "&lt").replace(">", "&gt")
        ss = "<a href='%s'> '%s' </a>" % (ts, ts)
        #ss = ss.replace("<", "&lt").replace(">", "&gt")
        rs.append(ss)

    return "<br>".join(rs)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


@app.before_request
def before_request():
    g.user = session.get('name')

@app.template_filter("dateFormat")
def data_format(s):
    try:
        t = float(s)
    except:
        return "NULL"
    return time.strftime("%Y-%m-%d", time.localtime(t))


@app.route("/index")
def get_index():
    return render_template("index.html")


@app.route("/frame")
def frame():
    return render_template("frame.html")


@app.route("/")
def index():
    return redirect(url_for("user.get"))


app.route("/test/test", endpoint="123", redirect_to='/')(None)


@app.route("/left")
def left():
    return render_template("fraleft.html")


@app.route("/copyright", methods=["GET", ])
def copyright():
    return render_template_string(u"<a href={{ url_for('index') }}> 主页 </a>")

if __name__ == "__main__":
    app.config.from_object("appcfg")
    app.run()

