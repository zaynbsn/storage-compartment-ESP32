from time import sleep_ms
from exemples.read import *
from homee import Homee

homee = Homee.defaultConfig()

#CheckInitialState().runAllTests(rfids=homee.rfidManager.boards)

try: 
    while True:
        if homee.wirelessManager.isConnected():
            homee.run()
        sleep_ms(250)

except KeyboardInterrupt:
    homee.stop()
    print('Bye')