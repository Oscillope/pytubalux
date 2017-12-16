import machine, neopixel

class Led:
    def __init__(self, scr, num, pin):
        self.screen = scr
        self.screen.print("{:d} leds, pin {:d}".format(num, pin))
        self.leds = neopixel.NeoPixel(machine.Pin(pin), num)
        self.leds.fill((0, 0, 0))
        self.leds.write()
        self.pattern_list = ["rainbow", "bounce", "cycle"]

    def patterns(self):
        return self.pattern_list

    def pat_set(self, idx):
        self.screen.print("Selected " + self.pattern_list[idx])

    def tempo_set(self, tempo):
        self.screen.print("Tempo: {:d}".format(tempo))
