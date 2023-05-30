from machine import Pin
from neopixel import NeoPixel

from rfids.rfid import Rfid
from rfids.rfidManager import RfidManager

from slots.slot import Slot
from slots.slotManager import SlotManager

from leds.led import Led
from leds.ledsManager import LedsManager

from ble.wireless_manager import *

class Homee:
    def __init__(self, slotManager, rfidManager, ledManager, wirelessManager):
        self.slotManager = slotManager
        self.rfidManager = rfidManager
        self.ledManager = ledManager
        self.wirelessManager = wirelessManager
        self.strToSend = ''

    def readAllBoards(self):
        self.rfidManager.readAllBoards()

    def updateSlotState(self):
        self.slotManager.updateSlotsStates()    

    def updateLedState(self):
        self.slotManager.updateLedsStates()

    def getRGBs(self):
        self.ledManager.getRGBs()

    def turnOnLeds(self):
        self.ledManager.turnOnLeds()

    def turnOffLed(self):
        self.ledManager.turnOffLeds()

    def getStrToSend(self):
        slotsStates = self.slotManager.getSlotsStates()
        self.strToSend = slotsStates[0] + "||" + slotsStates[1] + "||" + slotsStates[2]

    def sendToBle(self):
        self.getStrToSend()
        self.wirelessManager.sendDataToBLE(self.strToSend)

    def run(self):
        self.readAllBoards()
        self.updateSlotState()
        # send ble
        # self.sendToBle()
        self.updateLedState()
        self.getRGBs()
        self.turnOnLeds()

    def stop(self):
        self.turnOffLed()

    @staticmethod
    def defaultConfig():
        class BLECallback(CommunicationCallback):
            def __init__(self, bleName='homee'):
                self.wirelessManager = None
                self.bleName = bleName

            def didReceiveCallback(self, value):
                print("received: " + bytes(value).decode())
                if bytes(value).decode() == 'ACK':
                    self.wirelessManager.sendDataToBLE('ACK')

        wirelessManager = WirelessManager(bleCallback=BLECallback())

        sck = Pin(18, Pin.OUT)
        mosi = Pin(23, Pin.OUT)
        miso = Pin(19, Pin.OUT)
        sda = Pin(5, Pin.OUT)
        sda2 = Pin(17, Pin.OUT)
        sda3 = Pin(16, Pin.OUT)

        board1 = Rfid(rid='board1', sda=sda, sck=sck, mosi=mosi, miso=miso)
        board2 = Rfid(rid='board2', sda=sda2, sck=sck, mosi=mosi, miso=miso)
        board3 = Rfid(rid='board3', sda=sda3, sck=sck, mosi=mosi, miso=miso)
        rfidManager = RfidManager( { 'board1': board1, 'board2': board2, 'board3': board3 } )

        ledStrip = NeoPixel(Pin(13), 12)
        led1 = Led([1, 2])
        led2 = Led([5, 6])
        led3 = Led([9, 10])
        leds = [led1, led2, led3]
        ledManager = LedsManager(ledStrip, leds)

        slot1 = Slot(rfid=board1, badgeId='0x3c2356f8', led=led1)
        slot2 = Slot(rfid=board2, badgeId='0x5a5512b1', led=led2)
        slot3 = Slot(rfid=board3, badgeId='0x63d858ac', led=led3)
        slotManager = SlotManager( { 'slot1': slot1, 'slot2': slot2, 'slot3': slot3 } )

        return Homee(slotManager=slotManager, rfidManager=rfidManager, ledManager=ledManager, wirelessManager=wirelessManager)