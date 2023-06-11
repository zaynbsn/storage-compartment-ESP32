from time import sleep_ms
from exemples.read import *
from omi import Omi
from tests.checkList import *

omi = Omi.defaultConfig()

# CheckInitialState().runAllTests(ledManager=omi.ledManager, rfids=omi.rfidManager.boards)

try: 
    while True:
        if omi.wirelessManager.isConnected():
            omi.run()
        sleep_ms(250)

except KeyboardInterrupt:
    omi.stop()
    print('Bye')