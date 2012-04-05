import urllib
import urllib2
import threading
import json

def login():
    post("http://127.0.0.1/user/", 
        {"username":"testA", "password":"123"}
    )


import cookielib

def post(url, data):
    cj = cookielib.CookieJar()
    data = urllib.urlencode(data)  
    req=urllib2.Request(url, data)
    #response = urllib2.urlopen(req)
    #enable cookie  
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))  
    urllib2.install_opener(opener)
    response = opener.open(req, data)  
    return response.read()  

g_count = 0
def run(*args, **kwargs):
    global g_count
    data = {"name":"444a1", "des": str(threading.current_thread().ident)}
    print data
    if g_count%2 == 0:     
        url = "http://127.0.0.1/base/add"
    else:
        url = "http://127.0.0.1/base/"
    g_count+=1

    j = post(url, data)
    if len(j) > 0:
        print json.loads(j)  

import time
if __name__ == "__main__":
    #login()
    time.sleep(1) 
    #t = threading.Thread(target=run)
    #t.start() 
    for i in xrange(0, 200):
        t = threading.Thread(target=run)
        t.start()

