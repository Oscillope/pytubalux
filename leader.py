import network
import socket
from disp import Display
ssid = 'tubanet'

screen = Display()
ap_if = network.WLAN(network.AP_IF)
ap_if.active(True)
screen.print("AP active")
ap_if.config(essid=ssid)
screen.print("SSID: " + ssid)
addr = '10.11.10.1'
ap_if.ifconfig((addr, '255.255.255.0', '10.11.10.1', '10.11.10.1'))
screen.print("IP: " + addr)
