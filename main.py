from disp import Display
from leds import Led
from buttons import Buttons
from leader import Leader
from member import Member
from utime import sleep
import machine
import uio
import ujson
import _thread

# Read conf
conffile = uio.open("config", 'r')
config = ujson.loads(conffile.read())
conffile.close()

# Init objects
screen = Display()
screen.print("TubaLux(tm)")
prog = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
if (prog.value() == 0):
    screen.print("Programming mode")
    sleep(1)
    import sys
    sys.exit()
leds = Led(screen, config["num_leds"], config["led_pin"])
menu_timer = machine.Timer(1)
btn1_mode = "pattern"
btn2_mode = "tempo"
tap_samples = []
tap_count = 0

def menu_timeout(timer):
    global btn1_mode
    global btn2_mode
    leds.pat_set(screen.getmenu())
    screen.drawtext()
    screen.softbtn(["Pattern", "Tempo"])
    btn1_mode = "pattern"
    btn2_mode = "tempo"
    leds.led_timer_start()

def tap_timeout():
    global btn1_mode
    global btn2_mode
    global tap_samples
    avg = 0
    for samp in tap_samples:
        avg = avg + samp
    avg = avg / len(tap_samples)
    screen.clearpopup()
    leds.tempo_set(int(avg * 10))
    screen.softbtn(["Pattern", "Tempo"])
    btn1_mode = "pattern"
    btn2_mode = "tempo"
    leds.led_timer_start()

def tap_thread(sample):
    global tap_count
    while (tap_count < 300):
        tap_count = tap_count + 1
        sleep(0.01)
    tap_timeout()

def softkey_up():
    screen.movemenu(-1)
    menu_timer.init(period=3000, mode=machine.Timer.ONE_SHOT, callback=menu_timeout)

def softkey_down():
    screen.movemenu(1)
    menu_timer.init(period=3000, mode=machine.Timer.ONE_SHOT, callback=menu_timeout)

def softkey_pattern():
    global btn1_mode
    global btn2_mode
    screen.menu(leds.patterns(), 0)
    screen.softbtn(["Up", "Down"])
    btn1_mode = "up"
    btn2_mode = "down"

def softkey_tap():
    global tap_samples
    global tap_count
    sample = tap_count
    tap_count = 0
    tap_samples.append(sample)
    screen.popup("Tap! {:d}".format(sample))
    #menu_timer.init(period=3000, mode=machine.Timer.ONE_SHOT, callback=tap_timeout)

def softkey_tempo():
    global btn1_mode
    global btn2_mode
    global tap_samples
    global tap_count
    tap_count = 0
    tap_samples = []
    screen.popup("Tap!")
    screen.softbtn(["", "Tap!"])
    btn1_mode = "none"
    btn2_mode = "tap"
    _thread.start_new_thread(tap_thread, (tap_samples,))
    #menu_timer.init(period=3000, mode=machine.Timer.ONE_SHOT, callback=tap_timeout)

def btn1_cb():
    leds.led_timer_stop()
    if (btn1_mode == "pattern"):
        softkey_pattern()
    elif (btn1_mode == "up"):
        softkey_up()
    else:
        screen.print("Button1 press?")

def btn2_cb():
    leds.led_timer_stop()
    if (btn2_mode == "tempo"):
        softkey_tempo()
    elif (btn2_mode == "down"):
        softkey_down()
    elif (btn2_mode == "tap"):
        softkey_tap()
    else:
        screen.print("Button2 press?")

btns = Buttons(screen, [(12, btn1_cb), (14, btn2_cb)])
screen.softbtn(["Pattern", "Speed"])
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

