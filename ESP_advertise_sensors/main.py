from machine import Pin, SoftI2C, sleep
from time import sleep_ms
from exemples.read import *
from rfidManager import RfidManager
from nfcBoard import NFCBoard
from tests.checkList import CheckInitialState
from wireless_manager import *

class BLECallback(CommunicationCallback):
    def __init__(self, bleName='homee'):
        self.wirelessManager = None
        self.bleName = bleName

    def didReceiveCallback(self, value):
        print("received: " + value)
        if value == 'ACK':
            self.wirelessManager.sendDataToBLE('ACK')

wirelessManager = WirelessManager(bleCallback=BLECallback())

sck = Pin(18, Pin.OUT)
mosi = Pin(23, Pin.OUT)
miso = Pin(19, Pin.OUT)
sda = Pin(5, Pin.OUT)
sda2 = Pin(17, Pin.OUT)


board1 = NFCBoard(rid='board1', sda=sda, sck=sck, mosi=mosi, miso=miso)
board2 = NFCBoard(rid='board2', sda=sda2, sck=sck, mosi=mosi, miso=miso)
#boards = { 'board1': board1 }
boards = { 'board1': board1, 'board2': board2 }

rfidManager = RfidManager(boards)
CheckInitialState().runAllTests(rfids=boards)

try: 
    while True: 
        #rfidManager.readboard('board1')
        #rfidManager.readboard('board2')
        rfidManager.readAllBoards()

        sleep_ms(200)

except KeyboardInterrupt:
    print('Bye')

# while True:
#     wirelessManager.process()
#     # if wirelessManager.isConnected():
#     #     #wirelessManager.sendDataToWS("shaking")
#     #     pass
#     # else:
#     #     pass

#     sleep_ms(200)
