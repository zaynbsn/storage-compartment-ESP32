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
        print("received: " + value)
        if value == 'ACK':
            self.wirelessManager.sendDataToBLE('ACK')

# wirelessManager = WirelessManager(bleCallback=BLECallback())

# sck = Pin(18, Pin.OUT)
# mosi = Pin(23, Pin.OUT)
# miso = Pin(19, Pin.OUT)
# sda = Pin(5, Pin.OUT)
# sda2 = Pin(17, Pin.OUT)


# board1 = Rfid(rid='board1', sda=sda, sck=sck, mosi=mosi, miso=miso)
# board2 = Rfid(rid='board2', sda=sda2, sck=sck, mosi=mosi, miso=miso)
# #boards = { 'board1': board1 }
# boards = { 'board1': board1, 'board2': board2 }

# rfidManager = RfidManager(boards)

# slot1 = Slot(rfid=board1, badgeId='0x', led=None)s
# slot2 = Slot(rfid=board2, badgeId='0x', led=None)
# slotManager = SlotManager( { 'slot1': slot1, 'slot2': slot2 } )

homee = Homee.defaultConfig(BLECallback)

CheckInitialState().runAllTests(rfids=homee.rfidManager.boards)

try: 
    while True: 
        #rfidManager.readboard('board1')
        #rfidManager.readboard('board2')
        # rfidManager.readAllBoards()
        if homee.wirelessManager.isConnected():
            homee.run()

        sleep_ms(200)

except KeyboardInterrupt:
    homee.stop()
    print('Bye')