import network
import socket
from utime import sleep

class Member:
    def __init__(self, scr):
        self.screen = scr

    def start(self, ssid):
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(ssid)
        sleep(0.5)
        if (sta_if.isconnected()):
            addr = sta_if.ifconfig()[0]
            self.screen.print("Connected!")
            self.screen.print("IP="+addr)
            return False
        else:
            return True
