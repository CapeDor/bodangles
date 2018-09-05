from gevent.pywsgi import WSGIServer
from app import app

print("Http server started :)")

httpServer = WSGIServer(('', 5000), app)
httpServer.serve_forever()
