import network
import socket
from utime import sleep
import uosc.client
import uosc.server
import _thread

class OscNode:
    def __init__(self, scr, leds):
        self.screen = scr
        self.leds = leds

    def osc_callback(self, time, msg):
        #print("Got OSC message " + str(msg))
        addr, tag, ctrls, src = msg
        srcaddr = src[0]
        if ("tubalux" in addr):
            value = ctrls[0]
            if ("color" in addr):
                self.leds.hue = value * 360
            elif ("intens" in addr):
                self.leds.intens = value
            elif ("tempo" in addr):
                self.leds.tempo = value
            elif ("pattern" in addr):
                if tag in 'if':
                    pat = int(value)
                    print("set pattern " + str(pat))
                    self.leds.active_pat = self.leds.patterns[pat]
                elif tag == 's':
                    self.leds.active_pat = value
                else:
                    print("Invalid pat type " + tag)
            elif ("oneshot" in addr):
                os = int(value)
                print("run oneshot " + str(os))
                self.leds.do_oneshot(self.leds.oneshots[os])

    def osc_listen(self, host):
        addr, port = host
        uosc.server.run_server(addr, port, callback=self.osc_callback)

    def start_listen(self, host):
        _thread.start_new_thread(self.osc_listen, (host,))

class Leader(OscNode):
    def __init__(self, scr, leds):
        OscNode.__init__(self, scr, leds)
        self.ap_if = network.WLAN(network.AP_IF)
        self.clients = {}

    def osc_callback(self, time, msg):
        addr, tag, ctrls, src = msg
        srcaddr = src[0]
        if ("tubalux" in addr):
            value = ctrls[0]
            for client in list(self.clients.values()):
                if (client.dest[0] != srcaddr):
                    client.send(addr, (tag, value))
        elif ("ping" in addr):
            if (srcaddr not in list(self.clients.keys())):
                self.screen.print("sta " + srcaddr)
                self.clients[srcaddr] = uosc.client.Client(srcaddr, 9009)
            for i, pattern in enumerate(self.leds.patterns):
                self.clients[srcaddr].send("/tubalux/patterns/{:d}".format(i), pattern)
            for i, oneshot in enumerate(self.leds.oneshots):
                self.clients[srcaddr].send("/tubalux/oneshots/{:d}".format(i), oneshot)
            self.clients[srcaddr].send("/tubalux/intens", self.leds.intens)
            self.clients[srcaddr].send("/tubalux/color", self.leds.hue / 360)
            self.clients[srcaddr].send("/tubalux/pattern", self.leds.active_pat)
        OscNode.osc_callback(self, time, msg)

    def start(self, ssid):
        self.ap_if.active(True)
        self.screen.print("AP active")
        self.ap_if.config(essid=ssid)
        self.screen.print("SSID: " + ssid)
        addr = '10.11.10.1'
        self.ap_if.ifconfig((addr, '255.255.255.0', '10.11.10.1', '10.11.10.1'))
        self.screen.print("IP: " + addr)
        self.start_listen((addr, 9000))

class Member(OscNode):
    def start(self, ssid):
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(ssid)
        sleep(0.5)
        if (sta_if.isconnected()):
            addr = sta_if.ifconfig()[0]
            self.screen.print("Connected!")
            self.screen.print("IP="+addr)
            self.start_listen((addr, 9009))
            uosc.client.send(('10.11.10.1', 9000), "/ping", 0)
            return False
        else:
            return True
