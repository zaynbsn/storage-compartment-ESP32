class LedsManager:
    def __init__(self, ledStrip, leds):
        self.ledStrip = ledStrip
        self.leds = leds
        self.turnOffLeds()

    def checkLedsStates(self):
        print('led1', type(self.leds[0].currentState))
        print('led2', type(self.leds[1].currentState))
        print('led3', type(self.leds[2].currentState))

    def turnOnLeds(self):
        # violet (129, 14, 219)
        # orange (220, 90, 0)
        self.ledStrip.write()
        pass

    def turnOffLeds(self):
        self.ledStrip.fill((0, 0, 0))
        self.ledStrip.write()

    def deinitAllPins(self):
        for led in self.leds:
            led.deinit_pwm_pins()
