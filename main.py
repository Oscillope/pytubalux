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
button_mode = "pat/tempo"
tap_samples = []
tap_count = 0

def menu_timeout(timer):
    global button_mode
    leds.pat_set(screen.getmenu())
    screen.drawtext()
    screen.softbtn(["Pattern", "Tempo"])
    button_mode = "pat/tempo"
    leds.led_timer_start()

def tap_timeout():
    global button_mode
    global tap_samples
    avg = 0
    for samp in tap_samples:
        avg = avg + samp
    avg = avg / len(tap_samples)
    screen.clearpopup()
    leds.tempo_set(int(avg * 10))
    screen.softbtn(["Pattern", "Tempo"])
    button_mode = "pat/tempo"
    leds.led_timer_start()

def tap_thread(timer):
    global tap_count
    if (tap_count < 200):
        tap_count = tap_count + 1
    else:
        menu_timer.deinit()
        tap_timeout()

def softkey_up():
    screen.movemenu(-1)
    menu_timer.init(period=2000, mode=machine.Timer.ONE_SHOT, callback=menu_timeout)

def softkey_down():
    screen.movemenu(1)
    menu_timer.init(period=2000, mode=machine.Timer.ONE_SHOT, callback=menu_timeout)

def softkey_pattern():
    global button_mode
    screen.menu(leds.patterns(), 0)
    screen.softbtn(["Up", "Down"])
    button_mode = "up/down"
    menu_timer.init(period=2000, mode=machine.Timer.ONE_SHOT, callback=menu_timeout)

def softkey_tap():
    global tap_samples
    global tap_count
    sample = tap_count
    tap_count = 0
    tap_samples.append(sample)
    screen.popup("Tap! {:d}".format(sample))

def softkey_tempo():
    global button_mode
    global tap_samples
    global tap_count
    tap_count = 0
    tap_samples = []
    screen.popup("Tap!")
    screen.softbtn(["", "Tap!"])
    button_mode = "tap"
    #_thread.start_new_thread(tap_thread, (tap_samples,))
    menu_timer.init(period=10, mode=machine.Timer.PERIODIC, callback=tap_thread)

def softkey_none():
    pass

button_callbacks = {
    "pat/tempo": (softkey_pattern, softkey_tempo),
    "up/down": (softkey_up, softkey_down),
    "tap": (softkey_none, softkey_tap)
}

def btn1_cb():
    leds.led_timer_stop()
    try:
        button_callbacks[button_mode][0]()
    except KeyError:
        screen.print("OOPS " + button_mode)

def btn2_cb():
    leds.led_timer_stop()
    try:
        button_callbacks[button_mode][1]()
    except KeyError:
        screen.print("OOPS " + button_mode)

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

