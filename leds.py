import machine, neopixel, math
from ucollections import OrderedDict
from utime import sleep
import _thread

class Led:
    def __init__(self, scr, num, pin, rings=None):
        self.screen = scr
        self.screen.print("{:d} leds, pin {:d}".format(num, pin))
        self.leds = neopixel.NeoPixel(machine.Pin(pin), num)
        self.leds.fill((0, 0, 0))
        self.leds.write()
        self.reverse = False
        self.pos = 0
        self._patterns = {
            "rainbow": self.pat_rainbow,
            "cylon": self.pat_bounce,
            "rainbow cylon": self.pat_rainbowcyl,
            "marquee": self.pat_marquee,
            "solid": self.pat_solid,
            "pulse": self.pat_pulse
        }
        if (rings):
            ring_pats = {
                "r_radar": self.pat_radar,
                "r_tunnel": self.pat_tunnel,
            }
            self.rings = rings
            self._patterns.update(ring_pats)
        else:
            self.rings = None
        self.hue = 0
        self._colors = OrderedDict([
            ("red", 0),
            ("orange", 30),
            ("yellow", 50),
            ("green", 120),
            ("blue", 240),
            ("indigo", 260),
            ("violet", 280)
        ])
        self.intens = 0.2   # 0-1, float
        self._active = self.pat_rainbow
        self.period = 20    # 10ths of a second
        self.stop_thread = False
        _thread.start_new_thread(self.led_timer_thread, (None,))

    def led_timer_thread(self, unused):
        while (not self.stop_thread):
            self.pos = (self.pos + 1) % self.leds.n
            self._active()
            sleep(self.period / 100)

    def led_timer_stop(self):
        self.stop_thread = True

    def led_timer_start(self):
        if (self.stop_thread):
            self.stop_thread = False
            _thread.start_new_thread(self.led_timer_thread, (None,))

    # RGB/HSV stuff from http://code.activestate.com/recipes/576919-python-rgb-and-hsv-conversion/
    def hsv2rgb(self, h, s, v):
        h = float(h)
        s = float(s)
        v = float(v)
        h60 = h / 60.0
        h60f = math.floor(h60)
        hi = int(h60f) % 6
        f = h60 - h60f
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        r, g, b = 0, 0, 0
        if hi == 0: r, g, b = v, t, p
        elif hi == 1: r, g, b = q, v, p
        elif hi == 2: r, g, b = p, v, t
        elif hi == 3: r, g, b = p, q, v
        elif hi == 4: r, g, b = t, p, v
        elif hi == 5: r, g, b = v, p, q
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        return r, g, b

    def rgb2hsv(self, r, g, b):
        r, g, b = r/255.0, g/255.0, b/255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx-mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g-b)/df) + 360) % 360
        elif mx == g:
            h = (60 * ((b-r)/df) + 120) % 360
        elif mx == b:
            h = (60 * ((r-g)/df) + 240) % 360
        if mx == 0:
            s = 0
        else:
            s = df/mx
        v = mx
        return h, s, v

    @property
    def patterns(self):
        return list(self._patterns.keys())

    @property
    def colors(self):
        return list(self._colors.keys())

    @property
    def color_str(self):
        try:
            return next(key for key, self.hue in self._colors.items())
        except StopIteration:
            return "red"

    @color_str.setter
    def color_str(self, name):
        self.hue = self._colors[name]

    @property
    def active_pat(self):
        try:
            return next(key for key, self._active in self._patterns.items())
        except StopIteration:
            raise ValueError

    @active_pat.setter
    def active_pat(self, name):
        self.screen.print("Selected " + name)
        self._active = self._patterns[name]
        self.led_timer_start()

    @property
    def tempo(self):
        return self.period

    @tempo.setter
    def tempo(self, tempo):
        self.screen.print("Tempo: {:d}".format(tempo))
        self.period = int(tempo/2)
        self.led_timer_start()

    def pat_rainbow(self):
        pos = self.pos
        num = self.leds.n
        step = 360 / num
        for i in range(0, num):
            hue = ((i + pos) * step) % 360
            rgb = self.hsv2rgb(hue, 1, self.intens)
            #print("hue {:f} pos {:d} rgb ".format(hue, self.pos) + str(rgb))
            self.leds[i] = rgb
        self.leds.write()

    def pat_bounce(self):
        pos = self.pos
        if (self.reverse):
            i = self.leds.n - pos - 1
        else:
            i = pos
        self.leds[i] = self.hsv2rgb(self.hue, 1, self.intens)
        self.leds.write()
        self.leds[i] = (0, 0, 0)
        if (pos == (self.leds.n - 1)):
            self.reverse = not self.reverse

    def pat_marquee(self):
        pos = self.pos
        num = self.leds.n
        for i in range(0, num):
            if ((i + pos) % 4 == 0):
                self.leds[i] = self.hsv2rgb(self.hue, 1, self.intens)
            else:
                self.leds[i] = (0, 0, 0)
        self.leds.write()

    def pat_rainbowcyl(self):
        pos = self.pos
        if (self.reverse):
            i = self.leds.n - pos - 1
        else:
            i = pos
        step = 360 / self.leds.n
        hue = (pos * step) % 360
        self.leds[i] = self.hsv2rgb(hue, 1, self.intens)
        self.leds.write()
        self.leds[i] = (0, 0, 0)
        if (pos == (self.leds.n - 1)):
            self.reverse = not self.reverse

    def pat_solid(self):
        self.leds.fill(self.hsv2rgb(self.hue, 1, self.intens))
        self.leds.write()
        self.led_timer_stop()

    def pat_pulse(self):
        pos = self.pos
        if (pos == 0):
            self.reverse = not self.reverse
        self.leds.fill(self.hsv2rgb(self.hue, 1, self.intens))
        if (not self.reverse):
            for i in range(pos - 8, pos):
                if (i >= 0):
                    self.leds[i] = self.hsv2rgb(self.hue, 1, self.intens / (2 ** (9 - (pos - i))))
            self.leds[pos] = (0, 0, 0)
        elif (pos < 8):
            for i in range(1, 9 - pos):
                self.leds[self.leds.n - i] = self.hsv2rgb(self.hue, 1, self.intens / (2 ** (9 - (i + pos))))
        self.leds.write()

    def pat_radar(self):
        self.leds.fill((0, 0, 0))
        for j, len in enumerate(self.rings):
            offset = sum(self.rings[:j])
            index = (self.pos % len) + offset
            self.leds[index] = self.hsv2rgb(self.hue, 1, self.intens)
        self.leds.write()

    def pat_tunnel(self):
        if (self.pos >= len(self.rings)):
            self.pos = 0
        self.leds.fill((0, 0, 0))
        ring = self.pos
        offset = sum(self.rings[:ring])
        for i in range(offset, offset + self.rings[ring]):
            self.leds[i] = self.hsv2rgb(self.hue, 1, self.intens)
        self.leds.write()
