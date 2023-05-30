from machine import Pin, SoftI2C, sleep
from time import sleep_ms
from exemples.read import *
from rfids.rfidManager import RfidManager
from rfids.rfid import Rfid
from slots.slot import Slot
from slots.slotManager import SlotManager
from wireless_manager import *
from tests.checkList import CheckInitialState
from homee import Homee

homee = Homee.defaultConfig()

#CheckInitialState().runAllTests(rfids=homee.rfidManager.boards)

try: 
    while True:
        homee.run()
        sleep_ms(500)

except KeyboardInterrupt:
    homee.stop()
    print('Bye')