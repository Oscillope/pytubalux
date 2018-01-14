import machine
import micropython
import _thread
micropython.alloc_emergency_exception_buf(100)

class Buttons:
    def __init__(self, btn_list):
        self.debounce_timer = machine.Timer(0)
        self.debounce_done = False
        self.debouncing = None
        _thread.start_new_thread(self.btn_thread, (None,))
        self.callbacks = {}
        for btn in btn_list:
            pin = machine.Pin(btn[0], machine.Pin.IN, machine.Pin.PULL_UP)
            pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.btn_isr)
            self.callbacks[str(pin)] = btn[1]
            print(str(self.callbacks[str(pin)]) + "  " + str(pin))

    def btn_thread(self, ignored):
        while True:
            if (self.debounce_done and self.debouncing):
                self.callbacks[str(self.debouncing)]()
                self.debouncing = None
                self.debounce_done = False

    def btn_isr(self, pin):
        state = machine.disable_irq()
        self.debouncing = pin
        self.debounce_timer.init(period=80, mode=machine.Timer.ONE_SHOT, callback=self.debounce)
        machine.enable_irq(state)

    def debounce(self, timer):
        state = machine.disable_irq()
        if (self.debouncing and self.debouncing.value() == 0):
            self.debounce_done = True
        else:
            self.debouncing = None
        machine.enable_irq(state)
