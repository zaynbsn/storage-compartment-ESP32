from machine import Pin, Timer
from neopixel import NeoPixel

from rfids.rfid import Rfid
from rfids.rfidManager import RfidManager

from slots.slotStates import *
from slots.slot import Slot
from slots.slotManager import SlotManager

from leds.led import Led
from leds.ledsManager import LedsManager


from ble.wireless_manager import *

from systemStates import *

from time import sleep_ms



class Omi:
    def __init__(self, slotManager, rfidManager, ledManager, wirelessManager):
        self.slotManager = slotManager
        self.rfidManager = rfidManager
        self.ledManager = ledManager
        self.wirelessManager = wirelessManager
        self.strToSend = ''
        self.previousStrSent = ''
        self.timer = Timer(0)

        self.state = SystemInitialState()
        self.state.context = self

    def updateState(self, newState):
        if type(newState) != type(self.state):
            self.state = newState
            self.state.context = self
            print("New State: ", self.state)

    def readAllBoards(self):
        self.rfidManager.readAllBoards()

    def updateSlotState(self):
        self.slotManager.updateSlotsStates()    

    def updateLedState(self):
        self.slotManager.updateLedsStates(self.state)

    def changeLedsColors(self):
        self.ledManager.changeLedsColors()

    def turnOnLeds(self):
        self.ledManager.turnOnLeds()

    def turnOffLed(self):
        self.ledManager.turnOffLeds()

    def updateLedStateWarning(self):
        self.slotManager.launchWarning()

    def launchWarning(self):
        self.slotManager.launchWarning()
        self.updateState(WarningState())

    def launchCooldown(self):
        print('helo launchcooldown')
        def stopCallBack(t):
            if type(self.state) == ExitState:
                print('helo EXITSTATE')
                self.stop()
            if type(self.state) == EntryState:
                print('helo ENTRYSTATE')
                slotsStates = self.slotManager.getSlotsStates()
                for slotState in slotsStates:
                    print(slotState, NotHereState)
                    if slotState == NotHereState: 
                        self.launchWarning()

        self.timer.init(mode=Timer.ONE_SHOT, period=20000, callback=stopCallBack)

    def getStrToSend(self):
        slotsStates = self.slotManager.getSlotsStates()
        for i in range(len(slotsStates)):
            if slotsStates[i] == NotHereState:
                slotsStates[i] = 0
            elif slotsStates[i] == HereOKState:
                slotsStates[i] = 1
            elif slotsStates[i] == HereNOKState:
                slotsStates[i] = 1
            else:
                slotsStates[i] = -1

        self.strToSend = str(slotsStates[2]) + "||" + str(slotsStates[1]) + "||" + str(slotsStates[0])
        # todo gestion dans wirelessManager

    def sendToBle(self, bypass=False):
        self.getStrToSend()
        if self.strToSend != self.previousStrSent or bypass:
            self.wirelessManager.sendDataToBLE(self.strToSend)
            self.previousStrSent = self.strToSend
            print('strToSend', self.strToSend)
            # todo gestion dans wirelessManager
    
    def sendOff(self):
        self.wirelessManager.sendDataToBLE('off')
        print('################### OFF SENT ##################')

    def isAllSlotFull(self):
        return self.slotManager.isAllSlotsFull()

    def run(self):
        self.state.run()

    def stop(self):
        self.sendOff()
        self.turnOffLed()
        self.updateState(SystemInitialState())

    @staticmethod
    def defaultConfig():
        class BLECallback(CommunicationCallback):
            def __init__(self, bleName='omi'):
                self.wirelessManager = None
                self.bleName = bleName

            def didReceiveCallback(self, value):
                print("received: " + bytes(value).decode())
                if bytes(value).decode() == 'ACK':
                    self.wirelessManager.sendDataToBLE('ACK')

                if bytes(value).decode() == 'Entry':
                    self.wirelessManager.receivedState = EntryState()
                elif bytes(value).decode() == 'Exit':
                    self.wirelessManager.receivedState = ExitState()
                else:
                    self.wirelessManager.receivedState = SystemInitialState()


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
        led1 = Led([0, 1, 2])
        led2 = Led([4, 5, 6, 7])
        led3 = Led([9, 10, 11])
        leds = [led1, led2, led3]
        ledManager = LedsManager(ledStrip, leds)

        slot1 = Slot(rfid=board1, badgeId='0x3c2356f8', led=led1)
        slot2 = Slot(rfid=board2, badgeId='0x5a5512b1', led=led2)
        slot3 = Slot(rfid=board3, badgeId='0x63d858ac', led=led3)
        slotManager = SlotManager( { 'slot1': slot1, 'slot2': slot2, 'slot3': slot3 } )

        omi =  Omi(slotManager=slotManager, rfidManager=rfidManager, ledManager=ledManager, wirelessManager=wirelessManager)
        wirelessManager.omi = omi
        return omi