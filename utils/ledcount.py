# simple script to count LEDs in a strip

from disp import Display
import neopixel, machine
from buttons import Buttons

screen = Display()
screen.print("LED count")

leds = neopixel.NeoPixel(machine.Pin(17), 256, timing=1)
leds.fill((0, 0, 0))
leds.write()

count = 0
screen.softbtn(["Count", str(count)])

def inc_one():
    global count
    leds[count] = (60, 60, 60)
    count += 1
    leds.write()
    screen.softbtn(["Count", str(count)])

def inc_ten():
    global count
    for i in range(count, count+10):
        leds[i] = (60, 60, 60)
    count += 10
    leds.write()
    screen.softbtn(["Count", str(count)])

btns = Buttons(screen, [(12, inc_one), (14, inc_ten)])

screen.print("+1     +10")
