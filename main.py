from disp import Display
from utime import sleep

oled = Display()

oled.print("test")
sleep(1)
oled.print("TubaLux(tm)")
for i in range(0, 100):
    oled.bar(i)
    sleep(0.01)
sleep(1)
oled.clearbar()
