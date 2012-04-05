from flask import Flask, render_template
from flask import session

app = Flask(__name__)
app.secret_key = "123"
@app.route("/")
def index():
    session["user"] = 123
    return render_template("test.html")

@app.route("/user/<int:uid>")
def A(uid):
    print uid

@app.route("/user/123")
def B():
    return "123"

app.run()

