import machine, neopixel, math
import _thread

class Led:
    def __init__(self, scr, num, pin):
        self.screen = scr
        self.screen.print("{:d} leds, pin {:d}".format(num, pin))
        self.leds = neopixel.NeoPixel(machine.Pin(pin), num)
        self.leds.fill((0, 0, 0))
        self.leds.write()
        self.reverse = False
        self.pos = 0
        self.pattern_list = {
            "rainbow": self.pat_rainbow,
            "cylon": self.pat_bounce,
            "rainbow cylon": self.pat_rainbowcyl,
            "marquee": self.pat_marquee,
            "solid": self.pat_solid,
            "pulse": self.pat_pulse
        }
        self.color = 0
        self.color_list = {
            "red": 0,
            "orange": 30,
            "yellow": 50,
            "green": 120,
            "blue": 240,
            "indigo": 260,
            "violet": 280
        }
        self.intens = 1.0
        self.active = self.pat_rainbow
        self.period = int(60000/(120 * 4))
        self.timer = machine.Timer(2)
        self.led_timer_start()

    def led_timer_stop(self):
        self.timer.deinit()

    def led_timer_start(self):
        self.timer.init(period=self.period, mode=machine.Timer.PERIODIC, callback=self.led_timer_cb)

    def led_timer_cb(self, timer):
        self.pos = (self.pos + 1) % self.leds.n
        _thread.start_new_thread(self.active, (self.pos, ))

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

    def patterns(self):
        return list(self.pattern_list.keys())

    def pat_set(self, name):
        self.screen.print("Selected " + name)
        self.active = self.pattern_list[name]

    def tempo_set(self, tempo):
        self.screen.print("Tempo: {:d}".format(tempo))
        self.period = int(tempo/2)
        self.led_timer_start()

    def color_set(self, color):
        self.screen.print("Color " + color + " " + str(self.color_list[color]))
        self.color = self.color_list[color]

    def intens_set(self, intens):
        self.screen.print("Intens " + intens)
        self.intens = float(intens)/100.0

    def pat_rainbow(self, pos):
        num = self.leds.n
        step = 360 / num
        for i in range(0, num):
            hue = ((i + pos) * step) % 360
            rgb = self.hsv2rgb(hue, 1, 0.2)
            #print("hue {:f} pos {:d} rgb ".format(hue, self.pos) + str(rgb))
            self.leds[i] = rgb
        self.leds.write()

    def pat_bounce(self, pos):
        if (self.reverse):
            i = self.leds.n - pos - 1
        else:
            i = pos
        self.leds[i] = self.hsv2rgb(self.color, 1, self.intens)
        self.leds.write()
        self.leds[i] = (0, 0, 0)
        if (pos == (self.leds.n - 1)):
            self.reverse = not self.reverse

    def pat_marquee(self, pos):
        num = self.leds.n
        if (self.color == 0):
            color = self.color_list["orange"]
        else:
            color = self.color
        for i in range(0, num):
            if ((i + pos) % 4 == 0):
                self.leds[i] = self.hsv2rgb(color, 1, self.intens)
            else:
                self.leds[i] = (0, 0, 0)
        self.leds.write()

    def pat_rainbowcyl(self, pos):
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

    def pat_solid(self, pos):
        self.leds.fill(self.hsv2rgb(self.color, 1, self.intens))
        self.leds.write()
        self.led_timer_stop()

    def pat_pulse(self, pos):
        if (pos == 0):
            self.reverse = not self.reverse
        self.leds.fill(self.hsv2rgb(self.color, 1, self.intens))
        if (not self.reverse):
            for i in range(pos - 8, pos):
                if (i >= 0):
                    self.leds[i] = self.hsv2rgb(self.color, 1, self.intens / (2 ** (9 - (pos - i))))
                    print("i {:d} pos {:d} intens {:f}".format(i, pos, (self.intens / (2 ** (9 - (pos - i))))))
            self.leds[pos] = (0, 0, 0)
        elif (pos < 8):
            for i in range(1, 9 - pos):
                self.leds[self.leds.n - i] = self.hsv2rgb(self.color, 1, self.intens / (2 ** (9 - (i + pos))))
        self.leds.write()

