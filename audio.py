import machine
from utime import sleep
import _thread

class Audio:
    def __init__(self, scr, cb):
        self.screen = scr
        self.callback = cb
        self.adc = machine.ADC(machine.Pin(34, machine.Pin.IN, machine.Pin.PULL_UP))
        self.value = self.adc.read()
        _thread.start_new_thread(self.adc_read_thread, (None,))

    def adc_read_thread(self, unused):
        print("Thread start")
        while True:
            self.value = self.adc.read()
            #self.screen.print(str(self.value))
            if (self.value == 0):
                self.callback()
            sleep(0.1)

