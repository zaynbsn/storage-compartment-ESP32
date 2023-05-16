from slotStates import *
from rfids.rfidStates import *
from leds.ledStates import *

class Slot:
    def __init__(self, rfid, badgeId, led):
        self.rfid = rfid
        self.badgeId = badgeId
        self.led = led
        self.currentState = InitialState()
        self.currentState.context = self

    def updateState(self, newState):
        if type(self.currentState) != newState:
            self.currentState = newState
            self.currentState.context = self
            print("New State: ", self.currentState)

    def checkState(self):
        if type(self.rfid.currentState) == NoReadState:
            self.updateState(NotHereState())

        if self.rfid.badgeId ==  self.badgeId:
            self.updateState(HereOKState())
        else:
            self.updateState(HereNOKState())

    def updateLedState(self):
        if type(self.currentState) == NotHereState:
            self.led.updateState(RedState())

        elif type(self.currentState) == HereOKState:
            self.led.updateState(GreenState())

        elif type(self.currentState) == HereNOKState:
            self.led.updateState(BlueState())