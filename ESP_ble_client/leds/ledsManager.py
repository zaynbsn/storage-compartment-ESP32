class LedsManager:
    def __init__(self, leds):
        self.leds = leds
        self.turnOffLeds()

    def turnOnLeds(self):
        for led in self.leds:
            led.turnOnLed()

    def turnOffLeds(self):
        for led in self.leds:
            led.turnOffLed()

    def deinitAllPins(self):
        for led in self.leds:
            led.deinit_pwm_pins()
