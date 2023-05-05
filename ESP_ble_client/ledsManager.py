class LedsManager:
    def __init__(self, leds):
        self.leds = leds

    def turnOnLeds(self):
        for led in self.leds:
            led.turnOnLed()

    def turnOffLeds(self):
        for led in self.leds:
            led.turnOffLed()

    def testLeds(self, nbRepeat=2):
        print("Testing leds")
        for led in self.leds:
            led.testLed(nbRepeat)