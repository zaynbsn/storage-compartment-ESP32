from time import sleep
from leds.ledStates import *


class LedTests:

    def __init__(self):
        pass

    def runLedTests(self, led):
        self.testLed(led)
        self.testUpdateStates(led)

    def testLed(self, Led):
        count = 0
        while True:
            Led.turnOnLed()
            sleep(1)
            Led.turnOffLed()
            sleep(1)
            count += 1
            if count >= 2:
                break

    def testUpdateStates(self, led):
        led.updateState(FullState())
        led.turnOnLed()
        sleep(1)

        led.updateState(EmptyState())
        led.turnOnLed()
        sleep(1)

        led.updateState(WrongItemState())
        led.turnOnLed()
        sleep(1)

        led.turnOffLed()