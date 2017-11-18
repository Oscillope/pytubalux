import network
import socket
from utime import sleep
from disp import Display

screen = Display()
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('tubanet')
screen.print("Finding leader...")
sleep(0.5)
if (sta_if.isconnected()):
    addr = sta_if.ifconfig()[0]
    screen.print("Connected!")
    screen.print("IP="+addr)
else:
    screen.print("Connection failed :(")
