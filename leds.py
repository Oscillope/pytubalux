import machine, neopixel

class Led:
    def __init__(self, scr, num, pin):
        self.screen = scr
        self.screen.print("{:d} leds, pin {:d}".format(num, pin))
        self.leds = neopixel.NeoPixel(machine.Pin(pin), num)
        self.leds.fill((0, 0, 0))
        self.leds.write()
