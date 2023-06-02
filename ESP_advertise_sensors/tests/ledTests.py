from time import sleep
from leds.ledStates import *

class LedTests:

    def __init__(self):
        pass

    def runLedTests(self, ledManager):
        self.testLed(ledManager)

    def testLed(self, ledManager):
        for led in ledManager.leds:
            led.updateState(GreenState())
        ledManager.run()
        sleep(1)

        for led in ledManager.leds:
            led.updateState(RedState())
        ledManager.run()
        sleep(1)

        for led in ledManager.leds:
            led.updateState(BlueState())
        ledManager.run()
        sleep(1)

        ledManager.turnOffLeds()