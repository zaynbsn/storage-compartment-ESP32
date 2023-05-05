from time import sleep
from tests.ledTest import testLed, testUpdateStates

def checkInitialState(leds):
    print('Bonjour, les tests vont commencer.')
    sleep(1)
    print('Verification des leds')
    for led in leds:
        testLed(led)
        testUpdateStates(led)
    print('Leds OK')
    sleep(1)
    #rfid check
    sleep(1)