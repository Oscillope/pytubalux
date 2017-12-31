import network
import socket
import uosc.server

class Leader:
    screen = None
    def __init__(self, scr):
        self.screen = scr

    def osc_callback(self, time, msg):
        print("Got OSC message " + str(msg))

    def start(self, ssid):
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(True)
        self.screen.print("AP active")
        ap_if.config(essid=ssid)
        self.screen.print("SSID: " + ssid)
        addr = '10.11.10.1'
        ap_if.ifconfig((addr, '255.255.255.0', '10.11.10.1', '10.11.10.1'))
        self.screen.print("IP: " + addr)
        uosc.server.run_server(addr, 9000, callback=self.osc_callback)
