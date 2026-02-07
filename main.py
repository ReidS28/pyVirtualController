from virtual_gamepad import VirtualGamepad
from web_server import WebServer
import time

gp1 = VirtualGamepad(0)
gp1.start()

server = WebServer([gp1])
server.start()

while True:
    time.sleep(1)
