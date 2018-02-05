import network
import socket
from utime import sleep
import uosc.client
import uosc.server
import _thread

class Member:
    def __init__(self, scr, leds):
        self.screen = scr
        self.leds = leds

    def osc_callback(self, time, msg):
        print("Got OSC message " + str(msg))
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

    def osc_listen(self, addr):
        uosc.server.run_server(addr, 9009, callback=self.osc_callback)

    def start(self, ssid):
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(ssid)
        sleep(0.5)
        if (sta_if.isconnected()):
            addr = sta_if.ifconfig()[0]
            self.screen.print("Connected!")
            self.screen.print("IP="+addr)
            _thread.start_new_thread(self.osc_listen, (addr, ))
            uosc.client.send(('10.11.10.1', 9000), "/ping", 0)
            return False
        else:
            return True
