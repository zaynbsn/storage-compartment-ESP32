from led import *

class LedManager:
    def __init__(self, leds):
        self.leds = leds

    def turnOnLeds(self):
        for led in self.leds:
            led.turnOnLed()

    def turnOffLeds(self):
        for led in self.leds:
            led.turnOffLed()