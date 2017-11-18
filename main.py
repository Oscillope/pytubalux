from disp import Display
from utime import sleep

screen = Display()

screen.print("TubaLux(tm)")
for i in range(0, 100):
    screen.bar(i)
    sleep(0.01)
sleep(1)
screen.clearbar()
screen.print("init")
