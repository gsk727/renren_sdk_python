#-*- coding:utf-8 -*-
from flask import Flask

import os

app = Flask(__name__)

i = 0


@app.route("/base/", methods=["GET", ])
def index():
    global i
    i = i + 1
    print os.getpid()
    return str(i)

if __name__ == "__main__":
    
    app.run(debug=True)
