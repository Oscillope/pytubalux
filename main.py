from disp import Display
from leds import Led
from leader import Leader
from member import Member
from utime import sleep
from machine import Pin
import uio
import ujson

screen = Display()

screen.print("TubaLux(tm)")
conffile = uio.open("config", 'r')
config = ujson.loads(conffile.read())
conffile.close()
screen.softbtn(0, "Pattern")
screen.softbtn(1, "Speed")
screen.print("I am " + config["mode"])
leds = Led(screen, config["num_leds"], config["led_pin"])
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
    #screen.menu(["wine", "eggs", "cheese", "milk"], 0)
