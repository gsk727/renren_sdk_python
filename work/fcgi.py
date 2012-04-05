# encoding: utf-8
#from main import app
from  main import app
from flup.server.fcgi import WSGIServer

#WSGIServer->TheadedServer->ThreadPool(minSpare, maxSpare) 
WSGIServer(app, bindAddress=("127.0.0.1", 5000), minSpare=1, maxSpare=1).run()
