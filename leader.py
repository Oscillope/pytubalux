import network
import socket

class Leader:
    screen = None
    def __init__(self, scr):
        self.screen = scr

    def start(self, ssid):
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(True)
        self.screen.print("AP active")
        ap_if.config(essid=ssid)
        self.screen.print("SSID: " + ssid)
        addr = '10.11.10.1'
        ap_if.ifconfig((addr, '255.255.255.0', '10.11.10.1', '10.11.10.1'))
        self.screen.print("IP: " + addr)
