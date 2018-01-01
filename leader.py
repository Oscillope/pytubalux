import network
import socket
import uosc.server
import uosc.client

class Leader:
    screen = None
    def __init__(self, scr, leds):
        self.screen = scr
        self.leds = leds
        self.ap_if = network.WLAN(network.AP_IF)
        self.clients = {}

    def osc_callback(self, time, msg):
        #print("Got OSC message " + str(msg))
        addr, tag, ctrls, src = msg
        srcaddr = src[0]
        if ("tubalux" in addr):
            value = ctrls[0]
            if ("color" in addr):
                self.leds.hue_set(value * 360)
            elif ("intens" in addr):
                self.leds.intens_set(value * 100)
            elif ("pattern" in addr):
                pat = int(value)
                print("set pattern " + str(pat))
                self.leds.pat_set(self.leds.patterns()[pat])
                if (self.clients[srcaddr]):
                    self.clients[srcaddr].send("/tubalux/status/pattern", self.leds.patterns()[pat])
            for client in self.clients:
                client.send(msg)
        elif ("ping" in addr):
            if (srcaddr not in list(self.clients.keys())):
                print("client " + str(src) + " wants to register")
                self.clients[srcaddr] = uosc.client.Client(srcaddr, 9009)
            for i, pattern in enumerate(self.leds.patterns()):
                self.clients[srcaddr].send("/tubalux/status/pattern/{:d}".format(i), pattern)

    def start(self, ssid):
        self.ap_if.active(True)
        self.screen.print("AP active")
        self.ap_if.config(essid=ssid)
        self.screen.print("SSID: " + ssid)
        addr = '10.11.10.1'
        self.ap_if.ifconfig((addr, '255.255.255.0', '10.11.10.1', '10.11.10.1'))
        self.screen.print("IP: " + addr)
        uosc.server.run_server(addr, 9000, callback=self.osc_callback)
