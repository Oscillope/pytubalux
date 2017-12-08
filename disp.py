# Various screen things
import machine
import ssd1306

rst = machine.Pin(16, machine.Pin.OUT)
rst.value(1)
i2c = machine.I2C(scl=machine.Pin(15), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

class Display:
    line = 0
    lines = [None] * 5

    def __init__(self):
        self.btns = ["A", "B"]
        self.clear()

    def clear(self):
        oled.fill(0)
        oled.hline(0, 51, 128, 1)
        oled.show()

    def print(self, text):
        self.lines[self.line] = text
        self.line = self.line + 1
        if (self.line > 4):
            self.line = 0
        self.drawtext()

    def drawtext(self):
        self.cleartext()
        ln = self.line
        for i in range(0, len(self.lines)):
            if self.lines[ln] is not None:
                oled.text(self.lines[ln], 0, i * 10)
            ln = ln + 1
            if (ln > 4):
                ln = 0
        oled.show()

    def cleartext(self):
        oled.fill_rect(0, 0, 128, 50, 0)

    def popup(self, text):
        oled.rect(5, 5, 118, 45, 1)
        oled.fill_rect(6, 6, 116, 43, 0)
        oled.text(text, 10, 25)
        oled.show()

    def clearpopup(self):
        self.drawtext()

    def menu(self, opts, sel):
        if (sel < 0):
            sel = 0
        elif (sel >= len(opts)):
            sel = sel % len(opts)
        oled.rect(5, 5, 118, 45, 1)
        oled.fill_rect(6, 6, 116, 43, 0)
        oled.fill_rect(7, 17, 114, 10, 1)
        oled.text(opts[sel], 8, 18, 0)
        if (sel > 0):
            oled.text(opts[sel - 1], 8, 8)
        if (len(opts) > sel + 1):
            oled.text(opts[sel + 1], 8, 28)
        if (len(opts) > sel + 2):
            oled.text(opts[sel + 2], 8, 38)
        oled.show()

    def bar(self, progress):
        if progress == 0:
            self.clearbar()
            return
        for i in range(4, 124):
            oled.pixel(i, 58, 1)
        for i in range(4, ((progress / 100) * 120) + 4):
            oled.pixel(i, 59, 1)
            oled.pixel(i, 60, 1)
            oled.pixel(i, 61, 1)
            oled.pixel(i, 62, 1)
        oled.show()

    def clearbar(self):
        oled.fill_rect(0, 52, 128, 11, 0)
        oled.show()

    def softbtn(self, btn, text):
        self.clearbar()
        if (btn == 0):
            self.btns[0] = text
        else:
            self.btns[1] = text
        oled.text(self.btns[0], 0, 54)
        oled.text(self.btns[1], 128 - (len(text) * 8), 54)
        oled.show()
