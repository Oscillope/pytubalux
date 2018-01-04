# tubalux
The Deluxe Brass Band Lighting System

This is a ever-expanding lighting system, aimed at providing an inexpensive, flexible way for a band to roll out synchronized lighting effects. It is based on the ESP32, a handy little microcontroller that has a built-in wifi radio. It is written in MicroPython.

## The Hardware
![ESP32 Pinout](https://ae01.alicdn.com/kf/HTB1tYN_SFXXXXa2XpXXq6xXFXXXl.jpg)
This is the board. It can be purchased from [AliExpress](https://www.aliexpress.com/item/Lolin-ESP32-OLED-V2-0-Pro-ESP32-OLED-wemos-pour-Arduino-ESP32-OLED-WiFi-Modules-Bluetooth/32824819112.html) for around $10! You can also get a variety of different lengths of WS2812 LED strips. Pretty much all of them are compatible with this system.

## The Language
I picked MicroPython for this because it's pretty widely-supported, looked like fun, and my Python skills could use a brush-up. You can get the latest binary from [the MicroPython site](https://micropython.org/download/#esp32). To flash MicroPython, you can almost follow the instructions for [the ESP8266](https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html), **HOWEVER** it's important to note that you need to change the starting address from 0 to 0x1000. You can see the syntax for this in esptool on the MicroPython downloads page. Most of the documentation for [the ESP8266](https://docs.micropython.org/en/latest/esp8266/index.html) will also work on the ESP32, though there isn't an official documentation.

## The Scripts
TODO: Document here the config file syntax, OSC syntax, and general project structure
