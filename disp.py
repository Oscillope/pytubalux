# Various screen things
import machine
import ssd1306

rst = machine.Pin(16, machine.Pin.OUT)
rst.value(1)
i2c = machine.I2C(scl=machine.Pin(15), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

class Display:
    line = 0
    lines = [None] * 4

    def __init__(self):
        oled.text('Hello, world!', 0, 0)
        oled.show()

    def clear(self):
        oled.fill(0)
        oled.show()

    def print(self, text):
        self.clear()
        self.lines[self.line] = text
        self.line = self.line + 1
        if (self.line > 3):
            self.line = 0
        ln = self.line
        for i in range(0, len(self.lines)):
            if self.lines[ln] is not None:
                oled.text(self.lines[ln], 0, i * 10)
            ln = ln + 1
            if (ln > 3):
                ln = 0
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
        for i in range(4, 124):
            for j in range(58, 63):
                oled.pixel(i, j, 0)
        oled.show()
