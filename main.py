from disp import Display
from leader import Leader
from member import Member
from utime import sleep
import uio
import ujson

screen = Display()

screen.print("TubaLux(tm)")
for i in range(0, 100):
    screen.bar(i)
    sleep(0.01)
sleep(1)
screen.clearbar()
screen.print("init")
conffile = uio.open("config", 'r')
config = ujson.loads(conffile.read())
conffile.close()
screen.print("I am " + config["mode"])
if (config["mode"] == "leader"):
    ap = Leader(screen)
    ap.start(config["ssid"])
    screen.softbtn(0, "Pattern")
    screen.softbtn(1, "Speed")
    screen.popup("Ready")
    sleep(2)
    screen.clearpopup()
elif (config["mode"] == "member"):
    sta = Member(screen)
    while (sta.start(config["ssid"])):
        screen.print("Waiting...")
        sleep(5)
