from virtual_gamepad import VirtualGamepad
from web_server import WebServer
import time

gp1 = VirtualGamepad(0, "fake_ds4_profile")
gp1.start()

gp2 = VirtualGamepad(0, "fake_ds4_profile")
gp2.start()

server1 = WebServer([gp1, gp2])
server1.start()

while True:
    time.sleep(1)
