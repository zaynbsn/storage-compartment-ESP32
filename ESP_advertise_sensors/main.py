from time import sleep_ms
from exemples.read import *
from homee import Homee
from tests.checkList import *

homee = Homee.defaultConfig()

CheckInitialState().runAllTests(ledManager=homee.ledManager, rfids=homee.rfidManager.boards)

try: 
    while True:
        if homee.wirelessManager.isConnected():
            homee.run()
        sleep_ms(250)

except KeyboardInterrupt:
    homee.stop()
    print('Bye')