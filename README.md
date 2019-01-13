# tubalux
The Deluxe Brass Band Lighting System

This is a ever-expanding lighting system, aimed at providing an inexpensive, flexible way for a band to roll out synchronized lighting effects. It is based on the ESP32, a handy little microcontroller that has a built-in wifi radio. It is written in MicroPython.

## The Hardware
![ESP32 Pinout](https://ae01.alicdn.com/kf/HTB1tYN_SFXXXXa2XpXXq6xXFXXXl.jpg)
This is the board. It can be purchased from [AliExpress](https://www.aliexpress.com/item/Lolin-ESP32-OLED-V2-0-Pro-ESP32-OLED-wemos-pour-Arduino-ESP32-OLED-WiFi-Modules-Bluetooth/32824819112.html) for around $10! You can also get a variety of different lengths of WS2812 LED strips. Pretty much all of them are compatible with this system.

## The Language
I picked MicroPython for this because it's pretty widely-supported, looked like fun, and my Python skills could use a brush-up. You can get the latest binary from [the MicroPython site](https://micropython.org/download/#esp32). To flash MicroPython, you can almost follow the instructions for [the ESP8266](https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html), **HOWEVER** it's important to note that you need to change the starting address from 0 to 0x1000. You can see the syntax for this in esptool on the MicroPython downloads page. The official [MicroPython Documentation](http://docs.micropython.org/en/latest/index.html) is helpful, and the "Quick Reference for the ESP8266" section mostly applies to the ESP32 port as well.

## The Scripts
There should be a file called `config` in the root directory of your MicroPython installation. It lists, in JSON format, the number of LEDs, controller mode, LED pin, and ESSID. See [config.example](https://github.com/Oscillope/tubalux/blob/master/config.example) for, well, an example...

I've found that in general, it works best to compile the scripts into the micropython distribution as opposed to running them from the filesystem. To do this, you'll need to symlink all of the .py files including the uosc/ directory (except main.py) and put the links in `micropython/ports/esp32/modules` (you must clone the ![main micropython repo](https://github.com/micropython/micropython) first). Follow the instructions for the ![ESP32 port](https://github.com/micropython/micropython/blob/master/ports/esp32/README.md) to build and load it.

If you don't feel like doing all that, you can just run `./deploy.sh <PORT>` with the serial port of your ESP32 (i.e. `/dev/ttyUSB0`), and it'll dump everything in the filesystem on your device. You can play around, but you may run into memory errors after a while.

TODO: Document here the OSC syntax, and general project structure
