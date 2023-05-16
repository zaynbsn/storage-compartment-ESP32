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


class BLECallback(CommunicationCallback):
    def __init__(self, bleName='homee'):
        self.wirelessManager = None
        self.bleName = bleName

    def didReceiveCallback(self, value):
        print("received: " + bytes(value).decode())
        if bytes(value).decode() == 'ACK':
            self.wirelessManager.sendDataToBLE('ACK')


homee = Homee.defaultConfig(BLECallback)

#CheckInitialState().runAllTests(rfids=homee.rfidManager.boards)

try: 
    while True: 
        #rfidManager.readboard('board1')
        #rfidManager.readboard('board2')
        # rfidManager.readAllBoards()
        #if homee.wirelessManager.isConnected():
        # homee.run()
        # print(homee.slotManager.slots)
        # print(homee.rfidManager.boards)
        homee.run()
        sleep_ms(500)

except KeyboardInterrupt:
    # homee.stop()
    print('Bye')