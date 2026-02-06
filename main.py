from virtual_gamepad import VirtualGamepad
from web_server import WebServer

server = WebServer(10)
server.run()

gp1 = VirtualGamepad(0)
gp1.start()