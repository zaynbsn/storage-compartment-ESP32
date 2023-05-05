from time import sleep
from ledStates import *

def testLed(Led):
    count = 0
    while True:
        Led.turnOnLed()
        sleep(1)
        Led.turnOffLed()
        sleep(1)
        count += 1
        if count >= 2:
            break

def testUpdateStates(led):
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