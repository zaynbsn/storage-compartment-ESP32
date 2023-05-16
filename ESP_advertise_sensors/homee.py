from machine import Pin
from rfids.rfid import Rfid
from rfids.rfidManager import RfidManager
from slots.slot import Slot
from slots.slotManager import SlotManager
from wireless_manager import *

class Homee:
    def __init__(self, slotManager, rfidManager, ledManager, wirelessManager):
        self.slotManager = slotManager
        self.rfidManager = rfidManager
        self.ledManager = ledManager
        self.wirelessManager = wirelessManager

    def readAllBoards(self):
        self.rfidManager.readAllBoards()

    def updateSlotState(self):
        self.slotManager.updateSlotsStates()    

    def updateLedState(self):
        self.slotManager.updateLedsStates()

    def turnOnLeds(self):
        self.ledManager.turnOnLeds()

    def turnOffLed(self):
        self.ledManager.turnOffLeds()

    def run(self):
        self.readAllBoards()
        self.updateSlotState()
        self.updateLedState()
        # send ble
        self.turnOnLeds()

    def stop(self):
        self.turnOffLed()

    @staticmethod
    def defaultConfig(bleCallback):
        wirelessManager = WirelessManager(bleCallback=bleCallback())

        sck = Pin(18, Pin.OUT)
        mosi = Pin(23, Pin.OUT)
        miso = Pin(19, Pin.OUT)
        sda = Pin(5, Pin.OUT)
        sda2 = Pin(17, Pin.OUT)

        board1 = Rfid(rid='board1', sda=sda, sck=sck, mosi=mosi, miso=miso)
        board2 = Rfid(rid='board2', sda=sda2, sck=sck, mosi=mosi, miso=miso)
        rfidManager = RfidManager( { 'board1': board1, 'board2': board2 } )

        slot1 = Slot(rfid=board1, badgeId='0x', led=None)
        slot2 = Slot(rfid=board2, badgeId='0x', led=None)
        slotManager = SlotManager( { 'slot1': slot1, 'slot2': slot2 } )

        return Homee(slotManager=slotManager, rfidManager=rfidManager, ledManager=None, wirelessManager=wirelessManager)