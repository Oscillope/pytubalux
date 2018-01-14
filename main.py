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
try:
    rings = config["rings"]
except KeyError:
    rings = None
leds = Led(screen, config["num_leds"], config["led_pin"], rings if rings else None)
menu_timer = machine.Timer(1)
button_mode = "pat/tempo"
last_mode = "pat/tempo"
tap_samples = []
tap_count = 0

def menu_timeout(timer):
    global button_mode
    screen.drawtext()
    if (prog.value() == 0):
        screen.print("color mode")
        screen.softbtn(["Color", "Intens."])
        button_mode = "color"
        return
    if (last_mode == "pat/tempo"):
        leds.active_pat = screen.menu_str
    elif (last_mode == "color"):
        leds.color_str = screen.menu_str
    elif (last_mode == "intens"):
        leds.intens = float(screen.menu_str) / 100
    screen.softbtn(["Pattern", "Tempo"])
    button_mode = "pat/tempo"

def tap_timeout():
    global button_mode
    global tap_samples
    avg = 0
    for samp in tap_samples:
        avg = avg + samp
    avg = avg / len(tap_samples)
    screen.clearpopup()
    leds.tempo = int(avg)
    screen.softbtn(["Pattern", "Tempo"])
    button_mode = "pat/tempo"
    leds.led_timer_start()

def tap_thread(timer):
    global tap_count
    if (tap_count < 200):
        tap_count = tap_count + 1
    else:
        menu_timer.deinit()
        tap_count = 0
        tap_timeout()

def softkey_up():
    try:
        screen.menu_pos -= 1
    except ValueError:
        pass
    menu_timer.init(period=2000, mode=machine.Timer.ONE_SHOT, callback=menu_timeout)

def softkey_down():
    try:
        screen.menu_pos += 1
    except ValueError:
        pass
    menu_timer.init(period=2000, mode=machine.Timer.ONE_SHOT, callback=menu_timeout)

def softkey_pattern():
    global button_mode
    global last_mode
    last_mode = button_mode
    screen.menu(leds.patterns, 0)
    screen.softbtn(["Up", "Down"])
    button_mode = "up/down"
    menu_timer.init(period=2000, mode=machine.Timer.ONE_SHOT, callback=menu_timeout)

def softkey_tap():
    global tap_samples
    global tap_count
    leds.led_timer_stop()
    sample = tap_count
    tap_count = 0
    tap_samples.append(sample)
    screen.popup("Tap! {:d}".format(len(tap_samples)))

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

def softkey_color():
    global button_mode
    global last_mode
    last_mode = button_mode
    screen.menu(leds.colors, 0)
    screen.softbtn(["Up", "Down"])
    button_mode = "up/down"
    menu_timer.init(period=2000, mode=machine.Timer.ONE_SHOT, callback=menu_timeout)

def softkey_intens():
    global button_mode
    global last_mode
    last_mode = "intens"
    screen.menu(["100", "50", "20", "10"], 0)
    screen.softbtn(["Up", "Down"])
    button_mode = "up/down"
    menu_timer.init(period=2000, mode=machine.Timer.ONE_SHOT, callback=menu_timeout)

def softkey_none():
    pass

button_callbacks = {
    "pat/tempo": (softkey_pattern, softkey_tempo),
    "up/down": (softkey_up, softkey_down),
    "tap": (softkey_none, softkey_tap),
    "color": (softkey_color, softkey_intens)
}

def btn1_cb():
    try:
        button_callbacks[button_mode][0]()
    except KeyError:
        screen.print("OOPS " + button_mode)

def btn2_cb():
    try:
        button_callbacks[button_mode][1]()
    except KeyError:
        screen.print("OOPS " + button_mode)

btns = Buttons(screen, [(12, btn1_cb), (14, btn2_cb)])
screen.softbtn(["Pattern", "Speed"])
screen.print("I am " + config["mode"])
if (config["mode"] == "leader"):
    ap = Leader(screen, leds)
    _thread.start_new_thread(ap.start, (config["ssid"],))
elif (config["mode"] == "member"):
    sta = Member(screen)
    while (sta.start(config["ssid"])):
        screen.print("Waiting...")
        sleep(5)
elif (config["mode"] == "self"):
    screen.print("Independent mode")

