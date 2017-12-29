import machine
import micropython
import _thread
micropython.alloc_emergency_exception_buf(100)

class Buttons:
    def __init__(self, scr, btn_list):
        self.screen = scr
        self.debounce_timer = machine.Timer(0)
        self.debouncing = 0
        self.callbacks = {}
        for btn in btn_list:
            pin = machine.Pin(btn[0], machine.Pin.IN, machine.Pin.PULL_UP)
            pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.btn_isr)
            self.callbacks[str(pin)] = btn[1]
            print(str(self.callbacks[str(pin)]) + "  " + str(pin))

    def btn_thread(self, pin):
        self.callbacks[str(pin)]()

    def btn_isr(self, pin):
        state = machine.disable_irq()
        self.debouncing = pin
        self.debounce_timer.init(period=80, mode=machine.Timer.ONE_SHOT, callback=self.debounce)
        machine.enable_irq(state)

    def debounce(self, timer):
        state = machine.disable_irq()
        if (self.debouncing.value() == 0):
            _thread.start_new_thread(self.btn_thread, (self.debouncing,))
        machine.enable_irq(state)
