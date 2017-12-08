from disp import Display
from leader import Leader
from member import Member
from utime import sleep
from encoder import encoder
from machine import Pin
import uio
import ujson
import _thread

def encoderThread(func):
    e = encoder(12, 14)
    btn = Pin(34, Pin.IN, Pin.PULL_UP)
    last = 0
    while True:
        value = e.getValue()
        if value != last:
            last = value
            func(value)
#        if (btn.value() == 1):
#            disp.clearpopup()
#            break
        sleep(0.1)

screen = Display()

screen.print("TubaLux(tm)")
conffile = uio.open("config", 'r')
config = ujson.loads(conffile.read())
conffile.close()
screen.softbtn(0, "Pattern")
screen.softbtn(1, "Speed")
screen.print("I am " + config["mode"])
if (config["mode"] == "leader"):
    ap = Leader(screen)
    ap.start(config["ssid"])
elif (config["mode"] == "member"):
    sta = Member(screen)
    while (sta.start(config["ssid"])):
        screen.print("Waiting...")
        sleep(5)
elif (config["mode"] == "self"):
    screen.print("Independent mode")
    screen.menu(["wine", "eggs", "cheese", "milk"], 0)
    _thread.start_new_thread(encoderThread, ((lambda x: screen.menu(["wine", "eggs", "cheese", "milk"], x)),))

while True:
    sleep(1)
